import datetime
import uuid

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class LeadQuerySet(models.QuerySet):
    def notificables(self):
        """Excluye leads marcados Descartado/Spam, que nunca deben generar
        ninguna notificación (instantánea, de resumen diario o de reunión)."""
        return self.exclude(estado=Lead.Estado.DESCARTADO)


class Lead(models.Model):
    class Estado(models.TextChoices):
        """El orden de declaración ES el orden del pipeline comercial: se usa
        para poblar el <select> del CRM y para ordenar la columna Estado en
        el dashboard (ver internal_leads_dashboard / leads_dashboard.html)."""

        DESCARTADO = "descartado", "Descartado/Spam"
        NUEVO = "nuevo", "Nuevo"
        CONTACTADO = "contactado", "Contactado"
        REUNION_CONFIRMADA = "reunion_confirmada", "Reunión Confirmada"
        DIAGNOSTICO_ENVIADO = "diagnostico_enviado", "Diagnóstico enviado"
        DIAGNOSTICO_REALIZADO = "diagnostico_realizado", "Diagnóstico realizado"
        PRE_IMPLEMENTACION = "pre_implementacion", "Pre-implementación"
        PENDIENTE_IMPLEMENTACION = (
            "pendiente_implementacion",
            "Pendiente de Implementación",
        )
        SERVICIO_REALIZADO = "servicio_realizado", "Servicio realizado"
        MANTENIMIENTO_PROGRAMADO = (
            "mantenimiento_programado",
            "Mantenimiento programado",
        )

    # Alias retrocompatible: views.lead_update_status y el admin siguen
    # leyendo Lead.ESTADO_CHOICES como una lista de tuplas (código, etiqueta).
    ESTADO_CHOICES = Estado.choices

    nombre = models.CharField(max_length=255)
    correo = models.EmailField()
    empresa = models.CharField(max_length=255)
    # E.164 completo con prefijo país (ej. "+573001234567"). Solo lo llena el
    # booking público; el flujo interno puede dejarlo vacío.
    telefono = models.CharField(max_length=32, blank=True, default="")
    mensaje = models.TextField(blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=32,
        choices=Estado.choices,
        default=Estado.NUEVO,
        db_index=True,
    )
    # Momento del último cambio de estado (no de creación). Es el ancla del
    # recordatorio diario de 7 días para leads en estado Nuevo: si el lead
    # vuelve a Nuevo, este campo se actualiza y el contador se reinicia.
    estado_actualizado_en = models.DateTimeField(null=True, blank=True, db_index=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    ip_origen = models.GenericIPAddressField(blank=True, null=True)

    # Reunión confirmada — cargada manualmente en el CRM. Vive en Lead (y no
    # en un modelo aparte) porque solo existe una reunión vigente por lead y
    # los tres recordatorios (3d/1d/90min) son todos relativos a este único
    # instante.
    meeting_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Fecha y hora de la reunión"
    )
    meeting_link = models.URLField(
        max_length=500, blank=True, default="", verbose_name="Enlace de la reunión"
    )

    objects = LeadQuerySet.as_manager()

    class Meta:
        verbose_name = "Lead"
        verbose_name_plural = "Leads"
        ordering = ["-creado_en"]

    def __str__(self):
        return f"{self.nombre} - {self.empresa} ({self.estado})"


class LeadEstadoHistory(models.Model):
    """Auditoría de cada transición de estado de un Lead."""

    class Origen(models.TextChoices):
        MANUAL = "MANUAL", "Manual"
        AUTOMATICO = "AUTO", "Automático"
        MIGRACION = "MIGRACION", "Migración"

    lead = models.ForeignKey(
        Lead, related_name="estado_history", on_delete=models.CASCADE
    )
    estado_anterior = models.CharField(max_length=32, blank=True, default="")
    estado_nuevo = models.CharField(max_length=32, choices=Lead.Estado.choices)
    cambiado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )
    origen = models.CharField(
        max_length=16, choices=Origen.choices, default=Origen.MANUAL
    )
    nota = models.TextField(blank=True, default="")
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Historial de estado del lead"
        verbose_name_plural = "Historial de estados de leads"
        ordering = ["-creado_en"]
        indexes = [models.Index(fields=["lead", "-creado_en"])]

    def __str__(self):
        return f"{self.lead_id}: {self.estado_anterior} -> {self.estado_nuevo}"


def validar_limite_ventanas(lead_id: int, *, exclude_pk: int | None = None) -> None:
    """Lanza ValidationError si el lead ya tiene MaintenanceWindow.MAX_POR_LEAD
    ventanas de mantenimiento. Único punto de verdad para el límite de 6 —
    se llama desde el form y desde MaintenanceWindow.clean()."""
    qs = MaintenanceWindow.objects.filter(lead_id=lead_id)
    if exclude_pk is not None:
        qs = qs.exclude(pk=exclude_pk)
    if qs.count() >= MaintenanceWindow.MAX_POR_LEAD:
        raise ValidationError(
            f"Este lead ya tiene el máximo de {MaintenanceWindow.MAX_POR_LEAD} "
            "ventanas de mantenimiento."
        )


class MaintenanceWindow(models.Model):
    """Ventana de mantenimiento programado (hasta 6 por lead)."""

    MAX_POR_LEAD = 6

    lead = models.ForeignKey(
        Lead, related_name="maintenance_windows", on_delete=models.CASCADE
    )
    scheduled_for = models.DateTimeField(
        db_index=True, verbose_name="Fecha y hora programada"
    )
    titulo = models.CharField(max_length=120, blank=True, default="")
    notas = models.TextField(blank=True, default="")
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Ventana de mantenimiento"
        verbose_name_plural = "Ventanas de mantenimiento"
        ordering = ["scheduled_for"]
        indexes = [models.Index(fields=["completed", "scheduled_for"])]
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(completed=False, completed_at__isnull=True)
                    | models.Q(completed=True, completed_at__isnull=False)
                ),
                name="mw_completed_at_coherente",
            )
        ]

    def clean(self):
        validar_limite_ventanas(self.lead_id, exclude_pk=self.pk)

    def marcar_completada(self, *, completada: bool) -> None:
        from django.utils import timezone

        self.completed = completada
        self.completed_at = timezone.now() if completada else None
        self.save(update_fields=["completed", "completed_at", "actualizado_en"])

    def __str__(self):
        return f"Mantenimiento {self.lead_id} - {self.scheduled_for:%Y-%m-%d %H:%M}"


class NotificationLog(models.Model):
    """Registro de deduplicación de notificaciones programadas (resumen
    diario, aviso de reunión inminente, diagnóstico completado). La
    restricción unique en dedupe_key es lo que garantiza, a nivel de base de
    datos, que un mismo evento nunca se notifique dos veces aunque compitan
    varios workers de django-q2."""

    class Kind(models.TextChoices):
        LEAD_NUEVO_RECORDATORIO = "LEAD_NUEVO_RECORDATORIO", "Recordatorio lead nuevo"
        REUNION_RECORDATORIO = "REUNION_RECORDATORIO", "Recordatorio de reunión"
        REUNION_INMINENTE = "REUNION_INMINENTE", "Reunión inminente (90 min)"
        MANTENIMIENTO_RECORDATORIO = (
            "MANTENIMIENTO_RECORDATORIO",
            "Recordatorio de mantenimiento",
        )
        DIAGNOSTICO_COMPLETADO = "DIAGNOSTICO_COMPLETADO", "Diagnóstico completado"
        AGENDAMIENTO_CLIENTE = (
            "AGENDAMIENTO_CLIENTE",
            "Confirmación al cliente (booking)",
        )
        AGENDAMIENTO_INTERNO = "AGENDAMIENTO_INTERNO", "Aviso interno (booking)"

    lead = models.ForeignKey(
        Lead,
        related_name="notification_logs",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    kind = models.CharField(max_length=40, choices=Kind.choices)
    dedupe_key = models.CharField(max_length=200, unique=True)
    detalle = models.JSONField(default=dict, blank=True)
    enviado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Registro de notificación"
        verbose_name_plural = "Registros de notificación"
        ordering = ["-enviado_en"]
        indexes = [
            models.Index(fields=["lead", "kind"]),
            models.Index(fields=["-enviado_en"]),
        ]

    def __str__(self):
        return self.dedupe_key


class Questionnaire(models.Model):
    """Diagnóstico técnico ligado a un Lead. URL pública = su UUID."""

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pendiente"
        COMPLETED = "COMPLETED", "Completado"

    class TrafficPattern(models.TextChoices):
        ALL_REAL_TIME = "ALL_REAL_TIME", "Todo en Tiempo Real"
        MOST_REAL_TIME = "MOST_REAL_TIME", "Mayormente en Tiempo Real"
        MOST_BATCH = "MOST_BATCH", "Mayormente por Lotes"
        ALL_BATCH = "ALL_BATCH", "Todo por Lotes"

    class AITask(models.TextChoices):
        TEXT_GENERATION_COMPREHENSION = (
            "TEXT_GENERATION_COMPREHENSION",
            "Generación y Comprensión de texto",
        )
        EMBEDDINGS_RAG = "EMBEDDINGS_RAG", "Embeddings y/o Técnicas RAG"
        CODE_GENERATION = "CODE_GENERATION", "Generación de código"
        IMAGE_READING_SCANNING = (
            "IMAGE_READING_SCANNING",
            "Lectura y/o escaneo de imágenes",
        )
        IMAGE_GENERATION = "IMAGE_GENERATION", "Generación de imágenes"
        VIDEO_GENERATION = "VIDEO_GENERATION", "Generación de Videos"

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    lead = models.ForeignKey(
        Lead,
        related_name="questionnaires",
        on_delete=models.CASCADE,
    )
    status = models.CharField(
        max_length=16,
        choices=Status.choices,
        default=Status.PENDING,
    )
    # Lista de proveedores actuales (OpenAI, Anthropic, ...). JSONField es más
    # limpio que un M2M: no requiere tabla extra, soporta lista de strings y
    # valida contra un set cerrado de opciones a nivel de formulario.
    current_providers = models.JSONField(default=list, blank=True)
    other_provider_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Nombre del proveedor alternativo",
    )
    monthly_spend = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    traffic_pattern = models.CharField(
        max_length=32,
        choices=TrafficPattern.choices,
        blank=True,
        default="",
    )
    ai_tasks = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Tareas y capacidades de IA",
    )
    submitted_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cuestionario"
        verbose_name_plural = "Cuestionarios"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"Cuestionario {self.id} ({self.get_status_display()})"


class ProcessInventory(models.Model):
    """Fila de la tabla dinámica de procesos dentro de un cuestionario."""

    class ExecutionType(models.TextChoices):
        REAL_TIME = "REAL_TIME", "Tiempo real"
        BATCH = "BATCH", "Procesamiento por lotes"

    questionnaire = models.ForeignKey(
        Questionnaire,
        related_name="processes",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255, verbose_name="Nombre del proceso")
    execution_type = models.CharField(
        max_length=16,
        choices=ExecutionType.choices,
        default=ExecutionType.REAL_TIME,
    )
    input_tokens = models.IntegerField(
        default=0,
        verbose_name="Tokens de entrada promedio",
    )
    output_tokens = models.IntegerField(
        default=0,
        verbose_name="Tokens de salida promedio",
    )
    peak_concurrency = models.IntegerField(
        null=True,
        blank=True,
        help_text="Pico de concurrencia (solo tiempo real).",
    )
    monthly_executions = models.IntegerField(
        null=True,
        blank=True,
        help_text="Ejecuciones mensuales (solo procesamiento por lotes).",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Proceso del inventario"
        verbose_name_plural = "Procesos del inventario"
        ordering = ["created_at"]
        indexes = [
            models.Index(fields=["execution_type"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.get_execution_type_display()})"


def metric_file_upload_path(instance, filename):
    """Genera una ruta aislada por UUID de cuestionario para cada archivo."""
    questionnaire_id = instance.questionnaire_id
    if questionnaire_id is None and instance.questionnaire:
        questionnaire_id = instance.questionnaire.id
    return f"metrics_uploads/{questionnaire_id}/{filename}"


class QuestionnaireMetricFile(models.Model):
    """Archivo de métricas adjunto a un cuestionario por parte del cliente."""

    questionnaire = models.ForeignKey(
        Questionnaire,
        related_name="metric_files",
        on_delete=models.CASCADE,
    )
    file = models.FileField(
        upload_to=metric_file_upload_path,
        verbose_name="Archivo de métricas",
    )
    original_name = models.CharField(
        max_length=255,
        verbose_name="Nombre original",
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Archivo de métricas"
        verbose_name_plural = "Archivos de métricas"
        ordering = ["uploaded_at"]

    def __str__(self):
        return f"{self.original_name} ({self.questionnaire_id})"


# ──────────────────────────────────────────────
# Booking público (/agendar/)
# ──────────────────────────────────────────────


class BookingConfig(models.Model):
    """Configuración singleton del booking público. pk fijo en 1 — se crea
    (junto a los DiaHorario) en la migración de datos 0007 y get_solo() lo
    recupera sin sorpresas. Los horarios de referencia SIEMPRE se interpretan
    en America/Bogota (settings.TIME_ZONE): el usuario elige su zona horaria
    solo para ver/comparar horas, nunca para redefinir la disponibilidad."""

    dias_apertura = models.PositiveIntegerField(
        default=30,
        help_text="Días que la agenda permanece abierta hacia el futuro.",
    )
    duracion_min = models.PositiveIntegerField(
        default=30,
        help_text="Duración de la reunión y del intervalo entre slots (min).",
    )
    anticipo_min = models.PositiveIntegerField(
        default=1440,
        help_text="Antelación mínima (min) que debe tener un slot reservable (mínimo 24hr = 1440 min).",
    )
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configuración del booking"
        verbose_name_plural = "Configuración del booking"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj = cls.objects.filter(pk=1).first()
        if obj is None:
            obj = cls(pk=1, anticipo_min=1440)
            obj.save()
        elif obj.anticipo_min < 1440:
            obj.anticipo_min = 1440
            obj.save(update_fields=["anticipo_min"])
        return obj

    def __str__(self):
        return f"BookingConfig (apertura {self.dias_apertura}d, {self.duracion_min}min)"


class DiaHorario(models.Model):
    """Horario semanal del booking, un row por día (0=Lunes ... 6=Domingo).
    Las horas son HORA COLOMBIA (America/Bogota) — la zona de referencia del
    negocio; el frontend las convierte a la zona horaria del visitante."""

    DIAS = (
        (0, "Lunes"),
        (1, "Martes"),
        (2, "Miércoles"),
        (3, "Jueves"),
        (4, "Viernes"),
        (5, "Sábado"),
        (6, "Domingo"),
    )

    dia = models.PositiveSmallIntegerField(choices=DIAS, unique=True)
    activo = models.BooleanField(default=True)
    hora_inicio = models.TimeField(default=datetime.time(9, 0))
    hora_fin = models.TimeField(default=datetime.time(18, 0))

    class Meta:
        verbose_name = "Día de horario"
        verbose_name_plural = "Días de horario"
        ordering = ["dia"]

    def clean(self):
        if self.activo and self.hora_inicio >= self.hora_fin:
            raise ValidationError("La hora de inicio debe ser menor a la hora de fin.")

    def __str__(self):
        return (
            f"{self.get_dia_display()} {self.hora_inicio:%H:%M}-{self.hora_fin:%H:%M}"
        )


class Appointment(models.Model):
    """Reserva hecha desde el booking público (/agendar/). Varios
    Appointments pueden colgar del mismo Lead (máx. 2 futuras por correo,
    validado en la vista); Lead.meeting_at se sincroniza con la próxima."""

    class Estado(models.TextChoices):
        CONFIRMADA = "confirmada", "Confirmada"
        CANCELADA = "cancelada", "Cancelada"

    lead = models.ForeignKey(
        Lead, related_name="appointments", on_delete=models.CASCADE
    )
    # SIEMPRE en UTC (USE_TZ=True); la zona_horaria es solo display.
    inicio = models.DateTimeField(db_index=True, verbose_name="Inicio (UTC)")
    fin = models.DateTimeField(verbose_name="Fin (UTC)")
    duracion_min = models.PositiveIntegerField(default=30)
    zona_horaria = models.CharField(max_length=64, default="America/Bogota")
    consentimiento = models.BooleanField(
        default=False,
        verbose_name="Consentimiento de contacto otorgado",
    )
    estado = models.CharField(
        max_length=16,
        choices=Estado.choices,
        default=Estado.CONFIRMADA,
        db_index=True,
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Agendamiento"
        verbose_name_plural = "Agendamientos"
        ordering = ["inicio"]
        constraints = [
            # Un solo host: no pueden competir dos reservas por el mismo
            # instante. Partial index — las canceladas liberan su slot.
            models.UniqueConstraint(
                fields=["inicio"],
                condition=models.Q(estado="confirmada"),
                name="appointment_slot_confirmado_unico",
            ),
        ]
        indexes = [
            models.Index(fields=["estado", "inicio"]),
        ]

    def clean(self):
        if self.fin and self.inicio and self.fin <= self.inicio:
            raise ValidationError("El fin debe ser posterior al inicio.")

    def __str__(self):
        return f"Agendamiento {self.lead_id} — {self.inicio:%Y-%m-%d %H:%M} ({self.estado})"

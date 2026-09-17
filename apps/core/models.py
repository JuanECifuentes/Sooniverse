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
        PENDIENTE_IMPLEMENTACION = "pendiente_implementacion", "Pendiente de Implementación"
        SERVICIO_REALIZADO = "servicio_realizado", "Servicio realizado"
        MANTENIMIENTO_PROGRAMADO = "mantenimiento_programado", "Mantenimiento programado"

    # Alias retrocompatible: views.lead_update_status y el admin siguen
    # leyendo Lead.ESTADO_CHOICES como una lista de tuplas (código, etiqueta).
    ESTADO_CHOICES = Estado.choices

    nombre = models.CharField(max_length=255)
    correo = models.EmailField()
    empresa = models.CharField(max_length=255)
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

    lead = models.ForeignKey(Lead, related_name="estado_history", on_delete=models.CASCADE)
    estado_anterior = models.CharField(max_length=32, blank=True, default="")
    estado_nuevo = models.CharField(max_length=32, choices=Lead.Estado.choices)
    cambiado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL
    )
    origen = models.CharField(max_length=16, choices=Origen.choices, default=Origen.MANUAL)
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
        MANTENIMIENTO_RECORDATORIO = "MANTENIMIENTO_RECORDATORIO", "Recordatorio de mantenimiento"
        DIAGNOSTICO_COMPLETADO = "DIAGNOSTICO_COMPLETADO", "Diagnóstico completado"

    lead = models.ForeignKey(
        Lead, related_name="notification_logs", null=True, blank=True, on_delete=models.CASCADE
    )
    kind = models.CharField(max_length=40, choices=Kind.choices)
    dedupe_key = models.CharField(max_length=200, unique=True)
    detalle = models.JSONField(default=dict, blank=True)
    enviado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Registro de notificación"
        verbose_name_plural = "Registros de notificación"
        ordering = ["-enviado_en"]
        indexes = [models.Index(fields=["lead", "kind"]), models.Index(fields=["-enviado_en"])]

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

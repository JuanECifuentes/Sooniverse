import uuid

from django.db import models


class Lead(models.Model):
    ESTADO_CHOICES = [
        ("nuevo", "Nuevo"),
        ("contactado", "Contactado"),
        ("en_proceso", "En proceso"),
        ("cerrado", "Cerrado"),
    ]

    nombre = models.CharField(max_length=255)
    correo = models.EmailField()
    empresa = models.CharField(max_length=255)
    mensaje = models.TextField(blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default="nuevo",
    )
    ip_origen = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        verbose_name = "Lead"
        verbose_name_plural = "Leads"
        ordering = ["-creado_en"]

    def __str__(self):
        return f"{self.nombre} - {self.empresa} ({self.estado})"


class Questionnaire(models.Model):
    """Diagnóstico técnico ligado a un Lead. URL pública = su UUID."""

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pendiente"
        COMPLETED = "COMPLETED", "Completado"

    class TrafficPattern(models.TextChoices):
        REAL_TIME_CONTINUOUS = "REAL_TIME_CONTINUOUS", "Tiempo real — Cargas continuas"
        REAL_TIME_BURSTY = "REAL_TIME_BURSTY", "Tiempo real — Tráfico en ráfagas"
        BATCH_SCHEDULED = "BATCH_SCHEDULED", "Lotes — Ejecuciones programadas"
        BATCH_ONDEMAND = "BATCH_ONDEMAND", "Lotes — Bajo demanda"

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

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

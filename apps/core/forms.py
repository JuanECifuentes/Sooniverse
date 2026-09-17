from pathlib import Path

from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory

from .models import (
    Lead,
    MaintenanceWindow,
    Questionnaire,
    ProcessInventory,
    QuestionnaireMetricFile,
    validar_limite_ventanas,
)


# Proveedores soportados por el diagnóstico. Mantener sincronizado con la UI.
PROVIDER_CHOICES = (
    ("OPENAI_CHATGPT", "OpenAI / ChatGPT"),
    ("ANTHROPIC_CLAUDE", "Anthropic / Claude"),
    ("GEMINI", "Gemini"),
    ("AZURE", "Azure"),
    ("DEEPSEEK", "DeepSeek"),
    ("QWEN", "Qwen"),
    ("OTHER", "Otro"),
)

AI_TASK_CHOICES = (
    ("TEXT_GENERATION_COMPREHENSION", "Generación y Comprensión de texto"),
    ("EMBEDDINGS_RAG", "Embeddings y/o Técnicas RAG"),
    ("CODE_GENERATION", "Generación de código"),
    ("IMAGE_READING_SCANNING", "Lectura y/o escaneo de imágenes"),
    ("IMAGE_GENERATION", "Generación de imágenes"),
    ("VIDEO_GENERATION", "Generación de Videos"),
)

METRIC_FILE_EXTENSIONS = (".csv", ".parquet", ".xls", ".xlsx")
MAX_METRIC_FILE_SIZE_MB = 50
MAX_METRIC_FILES = 10


class LeadForm(forms.ModelForm):
    """Public contact form (landing). Honeypot-protected."""

    website_verification = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "style": "display:none !important;",
                "autocomplete": "off",
                "tabindex": "-1",
            }
        ),
        label="",
    )

    class Meta:
        model = Lead
        fields = ["nombre", "correo", "empresa", "mensaje"]
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "placeholder": "Nombre completo",
                    "class": "w-full rounded-lg bg-deep border border-border px-5 py-3.5 text-sm text-white placeholder-slate focus:outline-none focus:border-cyan transition",
                }
            ),
            "correo": forms.EmailInput(
                attrs={
                    "placeholder": "tu@empresa.com",
                    "class": "w-full rounded-lg bg-deep border border-border px-5 py-3.5 text-sm text-white placeholder-slate focus:outline-none focus:border-cyan transition",
                }
            ),
            "empresa": forms.TextInput(
                attrs={
                    "placeholder": "Nombre de la empresa",
                    "class": "w-full rounded-lg bg-deep border border-border px-5 py-3.5 text-sm text-white placeholder-slate focus:outline-none focus:border-cyan transition",
                }
            ),
            "mensaje": forms.Textarea(
                attrs={
                    "placeholder": "Cuéntanos sobre tu infraestructura de IA (opcional)",
                    "rows": 3,
                    "class": "w-full rounded-lg bg-deep border border-border px-5 py-3.5 text-sm text-white placeholder-slate focus:outline-none focus:border-cyan transition resize-none",
                }
            ),
        }
        error_messages = {
            "nombre": {
                "required": "El nombre es obligatorio para verificar su identidad en el sistema."
            },
            "correo": {
                "required": "La dirección de correo es obligatoria para establecer el canal de comunicación.",
                "invalid": "El correo electrónico ingresado no posee un formato válido para iniciar comunicación.",
            },
            "empresa": {
                "required": "El nombre de la empresa es obligatorio para contextualizar el diagnóstico tecnológico."
            },
        }

    def clean_correo(self):
        correo = self.cleaned_data.get("correo")
        if not correo:
            return correo
        import re

        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, correo):
            raise ValidationError(
                "El correo electrónico ingresado no posee un formato válido para iniciar comunicación."
            )
        try:
            validate_email(correo)
        except ValidationError:
            raise ValidationError(
                "El correo electrónico ingresado no posee un formato válido para iniciar comunicación."
            )

        from django.utils import timezone
        from datetime import timedelta

        time_threshold = timezone.now() - timedelta(hours=24)
        if Lead.objects.filter(
            correo__iexact=correo, creado_en__gte=time_threshold
        ).exists():
            raise ValidationError(
                "Ya ha sido registrada una solicitud para este cliente."
            )
        return correo

    def clean_website_verification(self):
        value = self.cleaned_data.get("website_verification")
        if value:
            raise ValidationError("Actividad de bot detectada. Petición rechazada.")
        return value


class InternalLeadForm(forms.ModelForm):
    """Form for internal Lead creation. Muted via skip_email_signal in the view."""

    # Crear un lead directamente en, por ejemplo, "Servicio realizado" no
    # tiene sentido — al crearlo manualmente solo caben estos 3 estados.
    ESTADOS_CREACION = (Lead.Estado.NUEVO, Lead.Estado.CONTACTADO, Lead.Estado.DESCARTADO)

    class Meta:
        model = Lead
        fields = ["nombre", "correo", "empresa", "mensaje", "estado"]
        widgets = {
            "nombre": forms.TextInput(
                attrs={
                    "placeholder": "Nombre completo",
                    "class": "w-full rounded-lg bg-deep border border-border px-4 py-3 text-sm text-white placeholder-slate focus:outline-none focus:border-cyan transition",
                }
            ),
            "correo": forms.EmailInput(
                attrs={
                    "placeholder": "tu@empresa.com",
                    "class": "w-full rounded-lg bg-deep border border-border px-4 py-3 text-sm text-white placeholder-slate focus:outline-none focus:border-cyan transition",
                }
            ),
            "empresa": forms.TextInput(
                attrs={
                    "placeholder": "Nombre de la empresa",
                    "class": "w-full rounded-lg bg-deep border border-border px-4 py-3 text-sm text-white placeholder-slate focus:outline-none focus:border-cyan transition",
                }
            ),
            "mensaje": forms.Textarea(
                attrs={
                    "placeholder": "Notas internas (opcional)",
                    "rows": 3,
                    "class": "w-full rounded-lg bg-deep border border-border px-4 py-3 text-sm text-white placeholder-slate focus:outline-none focus:border-cyan transition resize-none",
                }
            ),
            "estado": forms.Select(
                attrs={
                    "class": "w-full rounded-lg bg-deep border border-border px-4 py-3 text-sm text-white focus:outline-none focus:border-cyan transition",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["estado"].choices = [
            (v, l) for v, l in Lead.Estado.choices if v in self.ESTADOS_CREACION
        ]


# Formato que produce <input type="datetime-local">. Django's default
# DATETIME_INPUT_FORMATS no incluye el separador "T" -> sin esto, ambos
# formularios de fecha/hora fallan siempre con "Enter a valid date/time".
DATETIME_LOCAL_FORMATS = ["%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M"]
DATETIME_LOCAL_WIDGET_ATTRS = {
    "type": "datetime-local",
    "class": "w-full rounded-lg bg-deep border border-border px-4 py-3 text-sm text-white focus:outline-none focus:border-cyan transition",
}


class LeadMeetingForm(forms.ModelForm):
    """Carga manual de la fecha/hora y el link de la Reunión Confirmada."""

    meeting_at = forms.DateTimeField(
        required=True,
        input_formats=DATETIME_LOCAL_FORMATS,
        widget=forms.DateTimeInput(attrs=DATETIME_LOCAL_WIDGET_ATTRS, format="%Y-%m-%dT%H:%M"),
        label="Fecha y hora de la reunión",
    )
    meeting_link = forms.URLField(
        required=True,
        widget=forms.URLInput(
            attrs={
                "placeholder": "https://meet.google.com/...",
                "class": "w-full rounded-lg bg-deep border border-border px-4 py-3 text-sm text-white placeholder-slate focus:outline-none focus:border-cyan transition",
            }
        ),
        label="Enlace de la reunión",
    )

    class Meta:
        model = Lead
        fields = ["meeting_at", "meeting_link"]


class MaintenanceWindowForm(forms.ModelForm):
    """Alta/edición de una ventana de mantenimiento (máx. 6 por lead)."""

    scheduled_for = forms.DateTimeField(
        required=True,
        input_formats=DATETIME_LOCAL_FORMATS,
        widget=forms.DateTimeInput(attrs=DATETIME_LOCAL_WIDGET_ATTRS, format="%Y-%m-%dT%H:%M"),
        label="Fecha y hora programada",
    )

    class Meta:
        model = MaintenanceWindow
        fields = ["scheduled_for", "titulo", "notas"]
        widgets = {
            "titulo": forms.TextInput(
                attrs={
                    "placeholder": "Título (opcional)",
                    "class": "w-full rounded-lg bg-deep border border-border px-4 py-3 text-sm text-white placeholder-slate focus:outline-none focus:border-cyan transition",
                }
            ),
            "notas": forms.Textarea(
                attrs={
                    "placeholder": "Notas (opcional)",
                    "rows": 2,
                    "class": "w-full rounded-lg bg-deep border border-border px-4 py-3 text-sm text-white placeholder-slate focus:outline-none focus:border-cyan transition resize-none",
                }
            ),
        }

    def __init__(self, *args, lead=None, **kwargs):
        self.lead = lead
        super().__init__(*args, **kwargs)
        if lead is not None and self.instance.pk is None:
            self.instance.lead = lead

    def clean(self):
        cleaned = super().clean()
        lead_id = self.lead.pk if self.lead is not None else self.instance.lead_id
        try:
            validar_limite_ventanas(lead_id, exclude_pk=self.instance.pk)
        except ValidationError as exc:
            raise forms.ValidationError(exc.message)
        return cleaned


class QuestionnaireFinanceForm(forms.ModelForm):
    """Finance & context block of the questionnaire (public)."""

    current_providers = forms.MultipleChoiceField(
        choices=PROVIDER_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Proveedores actuales de API de IA",
    )
    other_provider_name = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Especifica el nombre del proveedor",
                "class": "w-full rounded-lg bg-deep border border-border px-4 py-3 text-sm text-white placeholder-slate focus:outline-none focus:border-cyan transition",
            }
        ),
        label="Nombre del proveedor alternativo",
    )
    monthly_spend = forms.DecimalField(
        required=False,
        max_digits=10,
        decimal_places=2,
        min_value=0,
        widget=forms.NumberInput(
            attrs={
                "placeholder": "0.00",
                "step": "0.01",
                "min": "0",
                "class": "w-full rounded-lg bg-deep border border-border px-4 py-3 text-sm text-white placeholder-slate focus:outline-none focus:border-cyan transition font-mono",
            }
        ),
        label="Gasto mensual estimado (USD)",
    )
    traffic_pattern = forms.ChoiceField(
        choices=Questionnaire.TrafficPattern.choices,
        required=False,
        widget=forms.RadioSelect,
        label="Patrón de tráfico predominante",
    )
    ai_tasks = forms.MultipleChoiceField(
        choices=AI_TASK_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Tareas y capacidades de IA que utilizas",
    )

    class Meta:
        model = Questionnaire
        fields = [
            "current_providers",
            "other_provider_name",
            "monthly_spend",
            "traffic_pattern",
            "ai_tasks",
        ]

    def clean_current_providers(self):
        value = self.cleaned_data.get("current_providers", [])
        return list(value)

    def clean_ai_tasks(self):
        value = self.cleaned_data.get("ai_tasks", [])
        return list(value)


class ProcessInventoryForm(forms.ModelForm):
    """Single row of the dynamic process table."""

    class Meta:
        model = ProcessInventory
        fields = [
            "name",
            "execution_type",
            "input_tokens",
            "output_tokens",
            "peak_concurrency",
            "monthly_executions",
        ]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Ej: Resumen de tickets",
                    "class": "w-full rounded-lg bg-deep border border-border px-3 py-2.5 text-sm text-white placeholder-slate focus:outline-none focus:border-cyan transition",
                }
            ),
            "execution_type": forms.Select(
                attrs={
                    "class": "w-full rounded-lg bg-deep border border-border px-3 py-2.5 text-sm text-white focus:outline-none focus:border-cyan transition js-exec-type",
                    "onchange": "toggleBatchFields(this)",
                }
            ),
            "input_tokens": forms.NumberInput(
                attrs={
                    "min": "0",
                    "placeholder": "0",
                    "class": "w-full rounded-lg bg-deep border border-border px-3 py-2.5 text-sm text-white placeholder-slate focus:outline-none focus:border-cyan transition font-mono",
                }
            ),
            "output_tokens": forms.NumberInput(
                attrs={
                    "min": "0",
                    "placeholder": "0",
                    "class": "w-full rounded-lg bg-deep border border-border px-3 py-2.5 text-sm text-white placeholder-slate focus:outline-none focus:border-cyan transition font-mono",
                }
            ),
            "peak_concurrency": forms.NumberInput(
                attrs={
                    "min": "0",
                    "placeholder": "—",
                    "class": "w-full rounded-lg bg-deep border border-border px-3 py-2.5 text-sm text-white placeholder-slate focus:outline-none focus:border-cyan transition font-mono js-peak",
                }
            ),
            "monthly_executions": forms.NumberInput(
                attrs={
                    "min": "0",
                    "placeholder": "—",
                    "class": "w-full rounded-lg bg-deep border border-border px-3 py-2.5 text-sm text-white placeholder-slate focus:outline-none focus:border-cyan transition font-mono js-batch",
                }
            ),
        }

    def clean(self):
        cleaned = super().clean()
        exec_type = cleaned.get("execution_type")
        if exec_type == ProcessInventory.ExecutionType.REAL_TIME and not cleaned.get(
            "peak_concurrency"
        ):
            self.add_error("peak_concurrency", "Requerido para tiempo real.")
        if exec_type == ProcessInventory.ExecutionType.BATCH and not cleaned.get(
            "monthly_executions"
        ):
            self.add_error(
                "monthly_executions", "Requerido para procesamiento por lotes."
            )
        return cleaned


class MultipleFileInput(forms.FileInput):
    """Widget que permite seleccionar varios archivos en un solo input."""

    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        attrs["multiple"] = True
        return super().render(name, value, attrs, renderer)

    def value_from_datadict(self, data, files, name):
        if not files:
            return None
        if hasattr(files, "getlist"):
            return files.getlist(name)
        return files.get(name)


class MultipleFileField(forms.FileField):
    """Campo de archivo que acepta y valida una lista de archivos."""

    widget = MultipleFileInput

    def to_python(self, data):
        if not data:
            return []
        if isinstance(data, list):
            return [super(MultipleFileField, self).to_python(item) for item in data]
        return [super().to_python(data)]

    def validate(self, value):
        if self.required and not value:
            raise ValidationError(self.error_messages["required"], code="required")
        for file in value:
            super().validate(file)


class QuestionnaireMetricFileForm(forms.Form):
    """Subida múltiple de archivos de métricas para un cuestionario."""

    metric_files = MultipleFileField(
        required=False,
        widget=MultipleFileInput(
            attrs={
                "accept": ",".join(METRIC_FILE_EXTENSIONS),
            }
        ),
        label="Adjuntar métricas de uso",
    )

    def clean_metric_files(self):
        files = self.cleaned_data.get("metric_files") or []
        if not isinstance(files, list):
            files = [files]
        files = list(files)
        if len(files) > MAX_METRIC_FILES:
            raise ValidationError(
                f"Puede adjuntar un máximo de {MAX_METRIC_FILES} archivos de métricas."
            )

        max_size = MAX_METRIC_FILE_SIZE_MB * 1024 * 1024
        for uploaded_file in files:
            ext = Path(uploaded_file.name).suffix.lower()
            if ext not in METRIC_FILE_EXTENSIONS:
                raise ValidationError(
                    f"Formato no permitido: {uploaded_file.name}. "
                    f"Solo se aceptan {', '.join(METRIC_FILE_EXTENSIONS)}."
                )
            if uploaded_file.size > max_size:
                raise ValidationError(
                    f"El archivo '{uploaded_file.name}' supera el límite de "
                    f"{MAX_METRIC_FILE_SIZE_MB} MB."
                )
        return files


ProcessInventoryFormSet = inlineformset_factory(
    Questionnaire,
    ProcessInventory,
    form=ProcessInventoryForm,
    fields=[
        "name",
        "execution_type",
        "input_tokens",
        "output_tokens",
        "peak_concurrency",
        "monthly_executions",
    ],
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=False,
)

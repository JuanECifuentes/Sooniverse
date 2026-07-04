from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Lead

class LeadForm(forms.ModelForm):
    # Honeypot field - bots will try to fill it
    website_verification = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'style': 'display:none !important;',
            'autocomplete': 'off',
            'tabindex': '-1',
        }),
        label=''
    )

    class Meta:
        model = Lead
        fields = ["nombre", "correo", "empresa", "mensaje"]
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Nombre completo',
                'class': 'w-full rounded-lg bg-deep border border-border px-5 py-3.5 text-sm text-white placeholder-slate focus:outline-none focus:border-cyan transition'
            }),
            'correo': forms.EmailInput(attrs={
                'placeholder': 'tu@empresa.com',
                'class': 'w-full rounded-lg bg-deep border border-border px-5 py-3.5 text-sm text-white placeholder-slate focus:outline-none focus:border-cyan transition'
            }),
            'empresa': forms.TextInput(attrs={
                'placeholder': 'Nombre de la empresa',
                'class': 'w-full rounded-lg bg-deep border border-border px-5 py-3.5 text-sm text-white placeholder-slate focus:outline-none focus:border-cyan transition'
            }),
            'mensaje': forms.Textarea(attrs={
                'placeholder': 'Cuéntanos sobre tu infraestructura de IA (opcional)',
                'rows': 3,
                'class': 'w-full rounded-lg bg-deep border border-border px-5 py-3.5 text-sm text-white placeholder-slate focus:outline-none focus:border-cyan transition resize-none'
            }),
        }
        error_messages = {
            'nombre': {
                'required': 'El nombre es obligatorio para verificar su identidad en el sistema.',
            },
            'correo': {
                'required': 'La dirección de correo es obligatoria para establecer el canal de comunicación.',
                'invalid': 'El correo electrónico ingresado no posee un formato válido para iniciar comunicación.',
            },
            'empresa': {
                'required': 'El nombre de la empresa es obligatorio para contextualizar el diagnóstico tecnológico.',
            },
        }

    def clean_correo(self):
        correo = self.cleaned_data.get('correo')
        if correo:
            try:
                validate_email(correo)
            except ValidationError:
                raise ValidationError('La dirección de correo electrónico ingresada no posee un formato válido para iniciar comunicación.')
        return correo

    def clean_website_verification(self):
        value = self.cleaned_data.get('website_verification')
        if value:
            # If filled, fail validation silently or raise validation error to stop processing
            raise ValidationError('Actividad de bot detectada. Petición rechazada.')
        return value

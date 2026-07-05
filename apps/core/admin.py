from django.contrib import admin
from .models import Lead

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("nombre", "correo", "empresa", "estado", "creado_en", "ip_origen")
    list_filter = ("estado", "creado_en")
    search_fields = ("nombre", "correo", "empresa", "mensaje")
    readonly_fields = ("creado_en", "ip_origen")
    ordering = ("-creado_en",)

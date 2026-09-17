from django.contrib import admin

from .models import (
    Appointment,
    BookingConfig,
    DiaHorario,
    Lead,
    LeadEstadoHistory,
    MaintenanceWindow,
    NotificationLog,
    ProcessInventory,
    Questionnaire,
)


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "correo",
        "empresa",
        "telefono",
        "estado",
        "creado_en",
        "estado_actualizado_en",
        "meeting_at",
        "ip_origen",
    )
    list_filter = ("estado", "creado_en")
    search_fields = ("nombre", "correo", "empresa", "mensaje")
    readonly_fields = ("creado_en", "actualizado_en", "ip_origen")
    ordering = ("-creado_en",)

    def save_model(self, request, obj, form, change):
        # Internal admin creation must not trigger automated emails.
        if not change:
            obj.skip_email_signal = True
        super().save_model(request, obj, form, change)


@admin.register(LeadEstadoHistory)
class LeadEstadoHistoryAdmin(admin.ModelAdmin):
    list_display = (
        "lead",
        "estado_anterior",
        "estado_nuevo",
        "origen",
        "cambiado_por",
        "creado_en",
    )
    list_filter = ("origen", "estado_nuevo")
    search_fields = ("lead__nombre", "lead__empresa")
    readonly_fields = ("creado_en",)
    ordering = ("-creado_en",)


@admin.register(MaintenanceWindow)
class MaintenanceWindowAdmin(admin.ModelAdmin):
    list_display = ("lead", "scheduled_for", "titulo", "completed", "completed_at")
    list_filter = ("completed",)
    search_fields = ("lead__nombre", "lead__empresa", "titulo")
    readonly_fields = ("creado_en", "actualizado_en")
    ordering = ("scheduled_for",)


@admin.register(NotificationLog)
class NotificationLogAdmin(admin.ModelAdmin):
    list_display = ("kind", "lead", "dedupe_key", "enviado_en")
    list_filter = ("kind",)
    search_fields = ("dedupe_key", "lead__nombre", "lead__empresa")
    readonly_fields = ("enviado_en",)
    ordering = ("-enviado_en",)


class ProcessInventoryInline(admin.TabularInline):
    model = ProcessInventory
    extra = 1
    readonly_fields = ("created_at", "updated_at")
    can_delete = True


@admin.register(Questionnaire)
class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "lead",
        "status",
        "traffic_pattern",
        "monthly_spend",
        "created_at",
        "submitted_at",
    )
    list_filter = ("status", "traffic_pattern", "created_at")
    search_fields = ("id", "lead__nombre", "lead__empresa", "lead__correo")
    readonly_fields = ("id", "created_at", "updated_at", "submitted_at")
    inlines = [ProcessInventoryInline]
    ordering = ("-created_at",)


@admin.register(ProcessInventory)
class ProcessInventoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "questionnaire",
        "execution_type",
        "input_tokens",
        "output_tokens",
        "peak_concurrency",
        "monthly_executions",
    )
    list_filter = ("execution_type",)
    search_fields = ("name", "questionnaire__id")
    readonly_fields = ("created_at", "updated_at")


admin.site.register(BookingConfig)


@admin.register(DiaHorario)
class DiaHorarioAdmin(admin.ModelAdmin):
    list_display = ("dia", "activo", "hora_inicio", "hora_fin")
    list_display_links = ("dia",)
    ordering = ("dia",)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "lead",
        "inicio",
        "fin",
        "zona_horaria",
        "consentimiento",
        "estado",
        "creado_en",
    )
    list_filter = ("estado", "consentimiento")
    search_fields = ("lead__nombre", "lead__correo", "lead__empresa")
    readonly_fields = ("creado_en",)
    ordering = ("-inicio",)

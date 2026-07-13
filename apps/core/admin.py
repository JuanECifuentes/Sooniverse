from django.contrib import admin

from .models import Lead, Questionnaire, ProcessInventory


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("nombre", "correo", "empresa", "estado", "creado_en", "ip_origen")
    list_filter = ("estado", "creado_en")
    search_fields = ("nombre", "correo", "empresa", "mensaje")
    readonly_fields = ("creado_en", "ip_origen")
    ordering = ("-creado_en",)

    def save_model(self, request, obj, form, change):
        # Internal admin creation must not trigger automated emails.
        if not change:
            obj.skip_email_signal = True
        super().save_model(request, obj, form, change)


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

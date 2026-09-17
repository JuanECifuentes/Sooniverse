"""Public and internal views for the core app."""

import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import FileResponse, Http404, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.templatetags.static import static
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_GET, require_http_methods
from django_q.tasks import async_task

from .forms import (
    AgendaDiaHorarioForm,
    BookingConfigForm,
    InternalLeadForm,
    LeadMeetingForm,
    MaintenanceWindowForm,
    ProcessInventoryFormSet,
    QuestionnaireFinanceForm,
    QuestionnaireMetricFileForm,
)
from .models import (
    Appointment,
    BookingConfig,
    DiaHorario,
    Lead,
    MaintenanceWindow,
    Questionnaire,
    QuestionnaireMetricFile,
)
from .services import booking as booking_svc
from .services.pipeline import transicionar_lead

logger = logging.getLogger("django.apps.core.views")


# ──────────────────────────────────────────────
# Public: landing + contact
# ──────────────────────────────────────────────


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def landing(request):
    return render(
        request,
        "core/landing.html",
        {"trm_contractual": getattr(settings, "TRM_CONTRACTUAL", 4100.0)},
    )


@require_GET
def manifest(request):
    data = {
        "name": "Sooniverse",
        "short_name": "Sooniverse",
        "description": "Servicios de Montaje de Plataformas Privadas de IA",
        "start_url": "/",
        "display": "browser",
        "background_color": "#070A12",
        "theme_color": "#00FF87",
        "orientation": "portrait",
        "icons": [
            {
                "src": static("icons/icon-144x144.png"),
                "sizes": "144x144",
                "type": "image/png",
            },
            {
                "src": static("icons/icon-192x192.png"),
                "sizes": "192x192",
                "type": "image/png",
                "purpose": "any",
            },
            {
                "src": static("icons/icon-512x512.png"),
                "sizes": "512x512",
                "type": "image/png",
                "purpose": "any",
            },
        ],
        "screenshots": [
            {
                "src": static("images/Captura_desktop.png"),
                "sizes": "1896x948",
                "type": "image/png",
                "form_factor": "wide",
                "label": "Vista escritorio",
            },
            {
                "src": static("images/Captura_mobile.png"),
                "sizes": "786x1580",
                "type": "image/png",
                "form_factor": "narrow",
                "label": "Vista móvil",
            },
        ],
    }
    return JsonResponse(data)


# ──────────────────────────────────────────────
# Internal: Lead CRUD + questionnaire management
# ──────────────────────────────────────────────


# Clase Tailwind de color por estado, usada por el renderer del <select> de
# estado en el dashboard (ver estado_choices_json más abajo).
ESTADO_CLASES = {
    Lead.Estado.DESCARTADO: "text-slate",
    Lead.Estado.NUEVO: "text-neon",
    Lead.Estado.CONTACTADO: "text-cyan",
    Lead.Estado.REUNION_CONFIRMADA: "text-cyan",
    Lead.Estado.DIAGNOSTICO_ENVIADO: "text-cyan",
    Lead.Estado.DIAGNOSTICO_REALIZADO: "text-cyan",
    Lead.Estado.PRE_IMPLEMENTACION: "text-violet",
    Lead.Estado.PENDIENTE_IMPLEMENTACION: "text-violet",
    Lead.Estado.SERVICIO_REALIZADO: "text-neon",
    Lead.Estado.MANTENIMIENTO_PROGRAMADO: "text-neon",
}


@login_required
def internal_leads_dashboard(request):
    """Internal Leads dashboard. Renders a list + create form + modal host."""
    if request.method == "POST":
        form = InternalLeadForm(request.POST)
        if form.is_valid():
            lead = form.save(commit=False)
            # Mute automated email notifications — internally created lead.
            lead.skip_email_signal = True
            lead.ip_origen = get_client_ip(request)
            lead.estado_actualizado_en = timezone.now()
            lead.save()
            messages.success(request, f"Lead interno creado: {lead.nombre}.")
            return redirect("core:internal_leads")
        messages.error(request, "Corrige los errores del formulario.")
    else:
        form = InternalLeadForm()

    leads = Lead.objects.all().prefetch_related("questionnaires", "maintenance_windows")
    leads_json = []
    for lead in leads:
        ventanas = list(lead.maintenance_windows.all())
        pendientes = [w for w in ventanas if not w.completed]
        proxima = min(pendientes, key=lambda w: w.scheduled_for) if pendientes else None
        entro_en = lead.estado_actualizado_en or lead.creado_en
        leads_json.append(
            {
                "id": lead.pk,
                "nombre": lead.nombre,
                "correo": lead.correo,
                "empresa": lead.empresa,
                "estado": lead.estado,
                "estado_display": lead.get_estado_display(),
                "creado_en": lead.creado_en.strftime("%Y-%m-%d %H:%M"),
                "estado_actualizado_en": entro_en.strftime("%Y-%m-%d %H:%M"),
                "dias_en_estado": (timezone.now() - entro_en).days,
                "meeting_at_iso": lead.meeting_at.isoformat()
                if lead.meeting_at
                else None,
                "meeting_at_display": (
                    timezone.localtime(lead.meeting_at).strftime("%Y-%m-%d %H:%M")
                    if lead.meeting_at
                    else None
                ),
                "meeting_link": lead.meeting_link,
                "ventanas_total": len(ventanas),
                "ventanas_pendientes": len(pendientes),
                "proxima_ventana": (
                    timezone.localtime(proxima.scheduled_for).strftime("%Y-%m-%d %H:%M")
                    if proxima
                    else None
                ),
            }
        )

    estado_choices_json = [
        {"value": v, "label": l, "cls": ESTADO_CLASES.get(v, "text-slate"), "orden": i}
        for i, (v, l) in enumerate(Lead.Estado.choices)
    ]

    return render(
        request,
        "core/internal/leads_dashboard.html",
        {
            "leads": leads,
            "leads_json": leads_json,
            "form": form,
            "estado_choices_json": estado_choices_json,
        },
    )


@login_required
@require_http_methods(["POST"])
def lead_update_status(request):
    """AJAX endpoint to update a Lead's estado. CSRF-protected and login-only."""
    lead_id = request.POST.get("lead_id")
    estado = request.POST.get("estado")
    valid_states = {code for code, _ in Lead.ESTADO_CHOICES}

    if not lead_id or estado not in valid_states:
        return JsonResponse(
            {"success": False, "message": "Petición inválida."}, status=400
        )

    lead = get_object_or_404(Lead, pk=lead_id)

    # Una reunión no puede confirmarse sin fecha: sin este guard, un lead
    # quedaría en "Reunión Confirmada" sin poder generar nunca recordatorios.
    if estado == Lead.Estado.REUNION_CONFIRMADA and lead.meeting_at is None:
        return JsonResponse(
            {
                "success": False,
                "requires": "meeting",
                "message": "Registra la fecha y el enlace de la reunión primero.",
            },
            status=400,
        )

    cambio = transicionar_lead(lead, estado, usuario=request.user)
    if not cambio:
        # No-op (ya estaba en ese estado): igual se responde success para
        # que el <select> no revierta visualmente.
        pass

    warn = None
    if (
        estado == Lead.Estado.MANTENIMIENTO_PROGRAMADO
        and not lead.maintenance_windows.exists()
    ):
        warn = (
            "El lead quedó en Mantenimiento programado sin ninguna ventana registrada."
        )

    response = {
        "success": True,
        "lead_id": lead.pk,
        "estado": lead.estado,
        "estado_display": lead.get_estado_display(),
        "estado_actualizado_en": lead.estado_actualizado_en.strftime("%Y-%m-%d %H:%M")
        if lead.estado_actualizado_en
        else None,
    }
    if warn:
        response["warn"] = warn
    return JsonResponse(response)


@login_required
@require_http_methods(["GET"])
def lead_detail_modal(request, lead_pk):
    """AJAX partial: modal 'Reunión / Mantenimiento' del lead (formulario de
    reunión, ventanas de mantenimiento e historial de estados)."""
    lead = get_object_or_404(Lead, pk=lead_pk)
    meeting_form = LeadMeetingForm(instance=lead)
    ventanas = lead.maintenance_windows.all()
    historial = lead.estado_history.all()[:20]
    return render(
        request,
        "core/internal/_lead_modal.html",
        {
            "lead": lead,
            "meeting_form": meeting_form,
            "ventanas": ventanas,
            "historial": historial,
            "max_ventanas": MaintenanceWindow.MAX_POR_LEAD,
        },
    )


@login_required
@require_http_methods(["POST"])
def lead_meeting_update(request, lead_pk):
    """Guarda fecha/hora + enlace de la reunión de un lead. Si se envía
    transicionar=1, también mueve el lead a Reunión Confirmada en el mismo
    round-trip (caso de uso normal desde el modal)."""
    lead = get_object_or_404(Lead, pk=lead_pk)
    form = LeadMeetingForm(request.POST, instance=lead)
    if not form.is_valid():
        return JsonResponse({"success": False, "errors": form.errors}, status=400)

    form.save()
    if request.POST.get("transicionar") == "1":
        transicionar_lead(lead, Lead.Estado.REUNION_CONFIRMADA, usuario=request.user)

    return JsonResponse(
        {
            "success": True,
            "meeting_at": timezone.localtime(lead.meeting_at).strftime(
                "%Y-%m-%d %H:%M"
            ),
            "meeting_link": lead.meeting_link,
            "estado": lead.estado,
            "estado_display": lead.get_estado_display(),
        }
    )


def _maintenance_rows_response(request, lead):
    ventanas = lead.maintenance_windows.all()
    return render(
        request,
        "core/internal/_maintenance_rows.html",
        {
            "lead": lead,
            "ventanas": ventanas,
            "max_ventanas": MaintenanceWindow.MAX_POR_LEAD,
        },
    )


@login_required
@require_http_methods(["POST"])
def maintenance_window_create(request, lead_pk):
    """Crea una ventana de mantenimiento (máx. 6 por lead, verificado bajo
    select_for_update para que dos altas concurrentes no pasen ambas el
    conteo)."""
    with transaction.atomic():
        lead = get_object_or_404(Lead.objects.select_for_update(), pk=lead_pk)
        form = MaintenanceWindowForm(request.POST, lead=lead)
        if not form.is_valid():
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
        form.save()

    return _maintenance_rows_response(request, lead)


@login_required
@require_http_methods(["POST"])
def maintenance_window_update(request, window_pk):
    """action=completar|reabrir|mover sobre una ventana existente."""
    window = get_object_or_404(MaintenanceWindow, pk=window_pk)
    action = request.POST.get("action")

    if action == "completar":
        window.marcar_completada(completada=True)
    elif action == "reabrir":
        window.marcar_completada(completada=False)
    elif action == "mover":
        form = MaintenanceWindowForm(request.POST, instance=window, lead=window.lead)
        if not form.is_valid():
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
        form.save()
    else:
        return JsonResponse(
            {"success": False, "message": "Acción inválida."}, status=400
        )

    return _maintenance_rows_response(request, window.lead)


@login_required
@require_http_methods(["POST"])
def maintenance_window_delete(request, window_pk):
    window = get_object_or_404(MaintenanceWindow, pk=window_pk)
    lead = window.lead
    window.delete()
    return _maintenance_rows_response(request, lead)


@login_required
@require_http_methods(["GET"])
def questionnaire_modal_partial(request, lead_pk):
    """AJAX partial rendered inside the 'Gestionar Cuestionarios' modal."""
    lead = get_object_or_404(Lead, pk=lead_pk)
    questionnaires = lead.questionnaires.all().order_by("-created_at")
    dummy_uuid = "00000000-0000-0000-0000-000000000000"
    public_base = request.build_absolute_uri(
        reverse("core:public_questionnaire", kwargs={"questionnaire_id": dummy_uuid})
    )
    public_url_template = public_base.replace(dummy_uuid, "{}")
    for q in questionnaires:
        q.public_url = public_url_template.format(q.id)
    return render(
        request,
        "core/internal/_questionnaire_modal.html",
        {
            "lead": lead,
            "questionnaires": questionnaires,
        },
    )


@login_required
@require_http_methods(["POST"])
def questionnaire_create(request, lead_pk):
    """Creates a new PENDING Questionnaire tied to the Lead (AJAX)."""
    lead = get_object_or_404(Lead, pk=lead_pk)
    questionnaire = Questionnaire.objects.create(
        lead=lead,
        status=Questionnaire.Status.PENDING,
    )
    public_url = request.build_absolute_uri(
        reverse(
            "core:public_questionnaire", kwargs={"questionnaire_id": questionnaire.id}
        )
    )
    return JsonResponse(
        {
            "success": True,
            "questionnaire_id": str(questionnaire.id),
            "status": questionnaire.status,
            "status_display": questionnaire.get_status_display(),
            "public_url": public_url,
            "created_at": questionnaire.created_at.isoformat(),
        }
    )


@login_required
@require_http_methods(["GET"])
def questionnaire_answers_partial(request, questionnaire_id):
    """Read-only snapshot of a COMPLETED questionnaire, rendered into a sub-modal."""
    # Strict UUID validation — any invalid uuid raises Http404 (no cross-uuid leakage).
    try:
        import uuid as _uuid

        qid = _uuid.UUID(str(questionnaire_id), version=4)
    except (ValueError, AttributeError, TypeError):
        raise Http404("Cuestionario no válido.")

    questionnaire = get_object_or_404(
        Questionnaire.objects.select_related("lead").prefetch_related("processes"),
        pk=qid,
    )
    processes = list(questionnaire.processes.all())
    processes_json = [
        {
            "name": p.name,
            "execution_type": p.execution_type,
            "execution_type_display": p.get_execution_type_display(),
            "input_tokens": p.input_tokens or 0,
            "output_tokens": p.output_tokens or 0,
            "peak_concurrency": p.peak_concurrency,
            "monthly_executions": p.monthly_executions,
        }
        for p in processes
    ]
    from apps.core.forms import AI_TASK_CHOICES, PROVIDER_CHOICES

    provider_map = dict(PROVIDER_CHOICES)
    task_map = dict(AI_TASK_CHOICES)

    display_providers = []
    for p in questionnaire.current_providers:
        name = provider_map.get(p, p)
        if p == "OTHER" and questionnaire.other_provider_name:
            name = f"Otro ({questionnaire.other_provider_name})"
        display_providers.append(name)

    display_tasks = [task_map.get(t, t) for t in questionnaire.ai_tasks]

    return render(
        request,
        "core/internal/_questionnaire_answers.html",
        {
            "questionnaire": questionnaire,
            "processes": processes,
            "processes_json": processes_json,
            "display_providers": display_providers,
            "display_tasks": display_tasks,
        },
    )


# ──────────────────────────────────────────────
# Internal: módulo Agenda (/interno/agenda/)
# ──────────────────────────────────────────────


@login_required
def internal_agenda(request):
    """Configuración del booking público + lista de próximas citas. Solo
    lectura de citas: la gestión del Lead vive en el dashboard de Leads."""
    config = BookingConfig.get_solo()

    if request.method == "POST":
        form = BookingConfigForm(request.POST, instance=config)
        filas = []
        valido_dias = True
        for dia in range(7):
            f = AgendaDiaHorarioForm(
                {
                    "dia": dia,
                    "activo": request.POST.get(f"dia_{dia}_activo", ""),
                    "hora_inicio": request.POST.get(f"dia_{dia}_inicio", ""),
                    "hora_fin": request.POST.get(f"dia_{dia}_fin", ""),
                }
            )
            if not f.is_valid():
                valido_dias = False
                for errs in f.errors.get("__all__", []):
                    messages.error(request, errs)
            filas.append(f)

        if valido_dias and form.is_valid():
            form.save()
            for f in filas:
                f.guardar()
            messages.success(request, "Configuración de la agenda guardada.")
            return redirect("core:internal_agenda")
        messages.error(request, "Revisa los campos marcados como inválidos.")
    else:
        form = BookingConfigForm(instance=config)
        filas = []
        for d in DiaHorario.objects.all().order_by("dia"):
            f = AgendaDiaHorarioForm(
                initial={
                    "dia": d.dia,
                    "activo": d.activo,
                    "hora_inicio": d.hora_inicio,
                    "hora_fin": d.hora_fin,
                }
            )
            filas.append(
                {
                    "form": f,
                    "nombre": d.get_dia_display(),
                    "dia": d.dia,
                    "activo": d.activo,
                    "inicio": d.hora_inicio.strftime("%H:%M"),
                    "fin": d.hora_fin.strftime("%H:%M"),
                }
            )

    citas_json = []
    for cita in (
        Appointment.objects.filter(
            estado=Appointment.Estado.CONFIRMADA, inicio__gte=timezone.now()
        )
        .select_related("lead")
        .order_by("inicio")[:50]
    ):
        p = booking_svc.presentar(cita.inicio, cita.zona_horaria)
        citas_json.append(
            {
                "id": cita.pk,
                "nombre": cita.lead.nombre,
                "email": cita.lead.correo,
                "empresa": cita.lead.empresa,
                "telefono": cita.lead.telefono,
                "bogota": p["bogota"],
                "visitante": f"{p['visitante']} ({cita.zona_horaria})",
                "creado_en": cita.creado_en.strftime("%Y-%m-%d %H:%M"),
                "lead_id": cita.lead_id,
            }
        )

    return render(
        request,
        "core/internal/agenda_dashboard.html",
        {
            "form": form,
            "filas_dias": filas,
            "config": config,
            "citas_json": citas_json,
            "zona_negocio": settings.TIME_ZONE,
        },
    )


# ──────────────────────────────────────────────
# Public: diagnostic questionnaire
# ──────────────────────────────────────────────


@require_http_methods(["GET", "POST"])
def public_questionnaire(request, questionnaire_id):
    """Public diagnostic questionnaire.

    PENDING  -> editable form (GET renders form, POST saves & flips to COMPLETED).
    COMPLETED-> immutable read-only render. Any POST is rejected silently.
    """
    # Strict UUID validation -> 404 otherwise (no UUID cross-talk possible).
    try:
        import uuid as _uuid

        qid = _uuid.UUID(str(questionnaire_id), version=4)
    except (ValueError, AttributeError, TypeError):
        raise Http404("Cuestionario no encontrado.")

    questionnaire = get_object_or_404(
        Questionnaire.objects.select_related("lead").prefetch_related("processes"),
        pk=qid,
    )

    readonly = questionnaire.status == Questionnaire.Status.COMPLETED

    # ── READ-ONLY MODE ─────────────────────────────────────────────
    if readonly or request.method == "GET":
        finance_form = QuestionnaireFinanceForm(instance=questionnaire)
        formset = ProcessInventoryFormSet(
            instance=questionnaire, queryset=questionnaire.processes.all()
        )
        metric_form = QuestionnaireMetricFileForm()
        return _render_questionnaire(
            request,
            questionnaire,
            finance_form,
            formset,
            metric_form,
            readonly=readonly,
        )

    # ── POST SUBMIT (only valid while PENDING) ──────────────────────
    if request.method == "POST" and not readonly:
        finance_form = QuestionnaireFinanceForm(request.POST, instance=questionnaire)
        formset = ProcessInventoryFormSet(
            request.POST, instance=questionnaire, queryset=questionnaire.processes.all()
        )
        metric_form = QuestionnaireMetricFileForm(
            request.POST or None, request.FILES or None
        )

        if finance_form.is_valid() and formset.is_valid() and metric_form.is_valid():
            with transaction.atomic():
                finance_form.save()
                formset.save()
                _save_metric_files(
                    questionnaire, metric_form.cleaned_data.get("metric_files", [])
                )
                questionnaire.status = Questionnaire.Status.COMPLETED
                questionnaire.submitted_at = timezone.now()
                questionnaire.save(
                    update_fields=[
                        "status",
                        "submitted_at",
                        "updated_at",
                        "current_providers",
                        "other_provider_name",
                        "monthly_spend",
                        "traffic_pattern",
                        "ai_tasks",
                    ]
                )

            # Notifica y transiciona el lead a "Diagnóstico realizado" en
            # segundo plano (no via post_save de Questionnaire, que dispararía
            # en cada guardado y el modelo tiene auto_now churn).
            transaction.on_commit(
                lambda: async_task(
                    "apps.core.tasks.notificar_diagnostico_completado",
                    str(questionnaire.id),
                )
            )

            # Re-render read-only confirmation view (immutable).
            finance_form = QuestionnaireFinanceForm(instance=questionnaire)
            formset = ProcessInventoryFormSet(
                instance=questionnaire, queryset=questionnaire.processes.all()
            )
            metric_form = QuestionnaireMetricFileForm()
            return _render_questionnaire(
                request,
                questionnaire,
                finance_form,
                formset,
                metric_form,
                readonly=True,
                just_submitted=True,
            )

        # Invalid: re-render editable with errors.
        logger.warning(
            f"Questionnaire {questionnaire.id} validation failed! "
            f"Finance errors: {finance_form.errors.as_json()}, "
            f"Formset errors: {formset.errors}, "
            f"Metric errors: {metric_form.errors.as_json()}"
        )
        return _render_questionnaire(
            request,
            questionnaire,
            finance_form,
            formset,
            metric_form,
            readonly=False,
        )

    # Defensive fallback.
    return redirect("core:public_questionnaire", questionnaire_id=str(questionnaire.id))


def _save_metric_files(questionnaire, files):
    """Persiste los archivos de métricas validados vinculados al cuestionario."""
    for uploaded_file in files:
        QuestionnaireMetricFile.objects.create(
            questionnaire=questionnaire,
            file=uploaded_file,
            original_name=uploaded_file.name,
        )


def _render_questionnaire(
    request,
    questionnaire,
    finance_form,
    formset,
    metric_form,
    *,
    readonly=False,
    just_submitted=False,
):
    return render(
        request,
        "core/diagnostico/cuestionario.html",
        {
            "questionnaire": questionnaire,
            "finance_form": finance_form,
            "formset": formset,
            "metric_form": metric_form,
            "metric_files": questionnaire.metric_files.all(),
            "readonly": readonly,
            "just_submitted": just_submitted,
            "empresa_nombre": questionnaire.lead.empresa,
        },
    )


@login_required
@require_GET
def download_metric_file(request, file_id):
    """Serves metric files securely only to logged in users."""
    metric_file = get_object_or_404(QuestionnaireMetricFile, pk=file_id)
    try:
        file_handle = metric_file.file.open()
    except FileNotFoundError:
        raise Http404("El archivo no existe.")

    response = FileResponse(file_handle, content_type="application/octet-stream")
    response["Content-Disposition"] = (
        f'attachment; filename="{metric_file.original_name}"'
    )
    return response

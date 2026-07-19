"""Public and internal views for the core app."""

import logging

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse, Http404, FileResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.core.cache import cache
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_GET, require_http_methods

from django.templatetags.static import static

from .forms import (
    InternalLeadForm,
    LeadForm,
    ProcessInventoryFormSet,
    QuestionnaireFinanceForm,
    QuestionnaireMetricFileForm,
)
from .models import Lead, Questionnaire, ProcessInventory, QuestionnaireMetricFile

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
    form = LeadForm()
    return render(
        request,
        "core/landing.html",
        {
            "trm_contractual": getattr(settings, "TRM_CONTRACTUAL", 4100.0),
            "form": form,
        },
    )


def contacto_lead(request):
    """POST handler for public contact. Email dispatch is centralized in the
    post_save signal (see apps.core.signals), so no manual async_task here."""
    if request.method != "POST":
        return redirect("core:landing")

    is_ajax = (
        request.headers.get("x-requested-with") == "XMLHttpRequest"
        or request.POST.get("ajax") == "true"
    )
    ip = get_client_ip(request)

    limit = getattr(settings, "RATE_LIMIT_LIMIT", 3)
    window = getattr(settings, "RATE_LIMIT_WINDOW", 600)
    cache_key = f"rate_limit_lead_{ip}"

    current_requests = cache.get(cache_key, 0)
    if current_requests >= limit:
        msg = "Límite de solicitudes excedido. Por motivos de ciberseguridad, intente de nuevo más tarde."
        logger.warning(f"Rate limit exceeded for IP: {ip}")
        if is_ajax:
            return JsonResponse({"success": False, "message": msg}, status=429)
        return redirect("/#contacto")

    form = LeadForm(request.POST)
    if form.is_valid():
        lead = form.save(commit=False)
        lead.ip_origen = ip
        lead.save()  # post_save signal enqueues notifications automatically

        cache.set(cache_key, current_requests + 1, timeout=window)

        logger.info(f"Lead {lead.pk} created; notifications dispatched via signal.")

        msg = "Su solicitud de diagnóstico ha sido registrada con éxito. Nos comunicaremos en menos de 24 horas."
        if is_ajax:
            return JsonResponse({"success": True, "message": msg})
        return redirect("/#contacto")

    error_msgs = []
    for field, errors in form.errors.items():
        for error in errors:
            error_msgs.append(error)
    msg_str = " ".join(error_msgs) or "Verifique los datos ingresados."
    logger.warning(f"Validation failed for lead submission from IP {ip}: {form.errors}")

    if is_ajax:
        return JsonResponse({"success": False, "message": msg_str}, status=400)
    return redirect("/#contacto")


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
            lead.save()
            messages.success(request, f"Lead interno creado: {lead.nombre}.")
            return redirect("core:internal_leads")
        messages.error(request, "Corrige los errores del formulario.")
    else:
        form = InternalLeadForm()

    leads = Lead.objects.all().prefetch_related("questionnaires")
    leads_json = [
        {
            "id": lead.pk,
            "nombre": lead.nombre,
            "correo": lead.correo,
            "empresa": lead.empresa,
            "estado": lead.estado,
            "estado_display": lead.get_estado_display(),
            "creado_en": lead.creado_en.strftime("%Y-%m-%d %H:%M"),
        }
        for lead in leads
    ]
    return render(
        request,
        "core/internal/leads_dashboard.html",
        {"leads": leads, "leads_json": leads_json, "form": form},
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
    lead.estado = estado
    lead.save(update_fields=["estado"])

    return JsonResponse(
        {
            "success": True,
            "lead_id": lead.pk,
            "estado": lead.estado,
            "estado_display": lead.get_estado_display(),
        }
    )


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
    from apps.core.forms import PROVIDER_CHOICES, AI_TASK_CHOICES

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
    response["Content-Disposition"] = f'attachment; filename="{metric_file.original_name}"'
    return response


"""Public views for the core app (Landing Page)."""

import logging
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.core.cache import cache
from django.views.decorators.http import require_GET
from django.templatetags.static import static
from django_q.tasks import async_task

from .forms import LeadForm
from .models import Lead

logger = logging.getLogger("django.apps.core.views")

def get_client_ip(request):
    """Extracts client IP address from request metadata."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip

def landing(request):
    """Render the public landing page."""
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
    """
    Handle POST submissions of the contact form.
    Applies rate limiting via Redis, validates the form (with honeypot),
    creates a Lead record, and triggers background email processing.
    """
    if request.method != "POST":
        return redirect("core:landing")

    is_ajax = request.headers.get("x-requested-with") == "XMLHttpRequest" or request.POST.get("ajax") == "true"
    ip = get_client_ip(request)

    # 1. Rate Limiting via Redis Cache
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

    # 2. Form Validation
    form = LeadForm(request.POST)
    if form.is_valid():
        lead = form.save(commit=False)
        lead.ip_origen = ip
        lead.save()

        # Increment rate limit counter
        cache.set(cache_key, current_requests + 1, timeout=window)

        # 3. Enqueue Async Task using Django Q2
        logger.info(f"Enqueuing async notification task for lead ID: {lead.id}")
        async_task("apps.core.tasks.procesar_nuevo_lead", lead.id)

        msg = "Su solicitud de diagnóstico ha sido registrada con éxito. Nos comunicaremos en menos de 24 horas."
        if is_ajax:
            return JsonResponse({"success": True, "message": msg})
        return redirect("/#contacto")
    else:
        # Collect errors
        error_msgs = []
        for field, errors in form.errors.items():
            for error in errors:
                error_msgs.append(error)
        
        msg_str = " ".join(error_msgs) or "Verifique los datos ingresados."
        logger.warning(f"Validation failed for lead submission from IP {ip}: {form.errors}")

        if is_ajax:
            return JsonResponse({"success": False, "message": msg_str}, status=400)
        
        # Standard POST redirect handling
        return redirect("/#contacto")


@require_GET
def manifest(request):
    """Serve the PWA manifest as JSON."""
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
            {"src": static("icons/icon-144x144.png"), "sizes": "144x144", "type": "image/png"},
            {"src": static("icons/icon-192x192.png"), "sizes": "192x192", "type": "image/png", "purpose": "any"},
            {"src": static("icons/icon-512x512.png"), "sizes": "512x512", "type": "image/png", "purpose": "any"},
        ],
        "screenshots": [
            {"src": static("images/Captura_desktop.png"), "sizes": "1896x948", "type": "image/png", "form_factor": "wide", "label": "Vista escritorio"},
            {"src": static("images/Captura_mobile.png"), "sizes": "786x1580", "type": "image/png", "form_factor": "narrow", "label": "Vista móvil"}
        ],
    }
    return JsonResponse(data)


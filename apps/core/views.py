"""Public views for the core app (Landing Page)."""

from django.conf import settings
from django.shortcuts import render


def landing(request):
    """Render the public landing page."""
    return render(
        request,
        "core/landing.html",
        {"trm_contractual": getattr(settings, "TRM_CONTRACTUAL", 4100.0)},
    )

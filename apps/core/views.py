"""Public views for the core app (Landing Page)."""

from django.shortcuts import render


def landing(request):
    """Render the public landing page."""
    return render(request, "core/landing.html")

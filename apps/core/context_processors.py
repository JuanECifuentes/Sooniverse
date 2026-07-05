from django.conf import settings

def django_env(request):
    """Exposes the active DJANGO_ENV setting to all templates."""
    return {
        "DJANGO_ENV": getattr(settings, "DJANGO_ENV", "local"),
    }

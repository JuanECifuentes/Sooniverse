from django.conf import settings


def django_env(request):
    """Exposes the active DJANGO_ENV setting, reCAPTCHA site key, and optional DEMO_URL
    to all templates."""
    return {
        "DJANGO_ENV": getattr(settings, "DJANGO_ENV", "local"),
        "RECAPTCHA_SITE_KEY": getattr(settings, "RECAPTCHA_SITE_KEY", ""),
        "DEMO_URL": getattr(settings, "DEMO_URL", "").strip(),
    }

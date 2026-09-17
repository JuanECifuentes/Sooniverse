from django.conf import settings


def django_env(request):
    """Exposes the active DJANGO_ENV setting and the reCAPTCHA site key
    (public, safe to expose) to all templates."""
    return {
        "DJANGO_ENV": getattr(settings, "DJANGO_ENV", "local"),
        "RECAPTCHA_SITE_KEY": getattr(settings, "RECAPTCHA_SITE_KEY", ""),
    }

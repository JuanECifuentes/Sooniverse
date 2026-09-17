import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger("django.apps.core.notifications")


def build_url(path: str = "") -> str:
    """Builds an absolute URL from settings.SITE_URL for use in contexts (like
    background tasks) where no `request` is available to call
    `request.build_absolute_uri`.

    Called as build_url("") (the common case, used as `base_url` in email
    contexts before an appended `{% url %}` tag, which always returns its
    own leading slash) it returns the bare origin with no trailing slash —
    e.g. "http://localhost:8000", never "http://localhost:8000/", which
    would otherwise double up into "...8000//interno/leads/"."""
    base = getattr(settings, "SITE_URL", "http://localhost:8000").rstrip("/")
    if not path:
        return base
    if not path.startswith("/"):
        path = f"/{path}"
    return f"{base}{path}"


def enviar_notificacion(
    destinatario: str,
    plantilla: str,
    asunto: str,
    contexto: dict,
    *,
    fail_silently: bool = True,
) -> bool:
    """
    Renders an HTML email template and sends it using the configured email backend.

    Returns True on a successful send, False on a handled failure (when
    `fail_silently=True`, the default — preserves the original behaviour of
    never raising). Pass `fail_silently=False` to have delivery failures
    propagate as exceptions instead — required by callers (like the daily
    digest) that need to distinguish "sent" from "not sent" to keep their own
    dedupe/claim bookkeeping correct.
    """
    try:
        # Render HTML template with context
        html_content = render_to_string(plantilla, contexto)
        # Strip HTML tags to create plain text version
        text_content = strip_tags(html_content)

        from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@sooniverse.com")

        # Create EmailMultiAlternatives message
        msg = EmailMultiAlternatives(
            subject=asunto,
            body=text_content,
            from_email=from_email,
            to=[destinatario],
        )
        msg.attach_alternative(html_content, "text/html")

        # Send mail
        msg.send(fail_silently=False)
        logger.info(f"Notification email sent successfully to {destinatario} (subject: '{asunto}').")
        return True
    except Exception as e:
        logger.error(
            f"Error sending notification email to {destinatario} (subject: '{asunto}'): {e}",
            exc_info=True,
        )
        if not fail_silently:
            raise
        return False

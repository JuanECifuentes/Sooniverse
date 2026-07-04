import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

logger = logging.getLogger("django.apps.core.notifications")

def enviar_notificacion(destinatario: str, plantilla: str, asunto: str, contexto: dict) -> None:
    """
    Renders an HTML email template and sends it using the configured email backend.
    Logs any errors without interrupting the execution flow.
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
    except Exception as e:
        logger.error(
            f"Error sending notification email to {destinatario} (subject: '{asunto}'): {e}",
            exc_info=True
        )

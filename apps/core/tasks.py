import logging
from django.conf import settings
from .models import Lead
from .services.notifications import enviar_notificacion

logger = logging.getLogger("django.apps.core.tasks")

def procesar_nuevo_lead(lead_id: int) -> None:
    """
    Task queued by Django Q2 to process a new lead submission.
    Fetches the Lead object from the database and sends:
    1. An internal notification email to the company/team.
    2. A confirmation email to the client who submitted the form.
    """
    try:
        lead = Lead.objects.get(pk=lead_id)
    except Lead.DoesNotExist:
        logger.error(f"Lead with ID {lead_id} does not exist. Aborting notifications.")
        return

    # Build context for the emails
    context = {
        "lead": lead,
        "nombre": lead.nombre,
        "correo": lead.correo,
        "empresa": lead.empresa,
        "mensaje": lead.mensaje or "Sin mensaje adicional.",
        "creado_en": lead.creado_en,
        "estado": lead.get_estado_display(),
        "ip_origen": lead.ip_origen,
    }

    # 1. Send Internal Notification
    destinatario_interno = getattr(settings, "NOTIFICACION_INTERNA_EMAIL", "soporte@sooniverse.com")
    asunto_interno = f"[Nuevo Lead] Registro de contacto: {lead.empresa}"
    plantilla_interna = "core/emails/notificacion_interna.html"
    
    logger.info(f"Sending internal notification for lead {lead_id} to {destinatario_interno}.")
    enviar_notificacion(
        destinatario=destinatario_interno,
        plantilla=plantilla_interna,
        asunto=asunto_interno,
        contexto=context,
    )

    # 2. Send Customer Confirmation
    asunto_cliente = "Diagnóstico Tecnológico de IA - Solicitud Recibida"
    plantilla_cliente = "core/emails/respuesta_cliente.html"
    
    logger.info(f"Sending customer confirmation for lead {lead_id} to {lead.correo}.")
    enviar_notificacion(
        destinatario=lead.correo,
        plantilla=plantilla_cliente,
        asunto=asunto_cliente,
        contexto=context,
    )

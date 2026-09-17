import logging
from datetime import timedelta

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from .models import Appointment, Lead, LeadEstadoHistory, NotificationLog, Questionnaire
from .services.booking import presentar
from .services.dedupe import reclamar
from .services.digest import construir_digest
from .services.notifications import build_url, enviar_notificacion
from .services.pipeline import transicionar_lead

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
        "base_url": build_url(""),
    }

    # 1. Send Internal Notification
    destinatario_interno = getattr(
        settings, "NOTIFICACION_INTERNA_EMAIL", "soporte@sooniverse.com"
    )
    asunto_interno = f"[Nuevo Lead] Registro de contacto: {lead.empresa}"
    plantilla_interna = "core/emails/notificacion_interna.html"

    logger.info(
        f"Sending internal notification for lead {lead_id} to {destinatario_interno}."
    )
    enviar_notificacion(
        destinatario=destinatario_interno,
        plantilla=plantilla_interna,
        asunto=asunto_interno,
        contexto=context,
    )

    # 2. Send Customer Confirmation
    # Nota: core/emails/respuesta_cliente.html se conserva intacta (no se
    # elimina) pero ya no se usa aquí; el flujo de "reservar una reunión"
    # usa la plantilla nueva reunion_agendada.html.
    asunto_cliente = "Tu reunión con Sooniverse está en camino"
    plantilla_cliente = "core/emails/reunion_agendada.html"

    logger.info(f"Sending customer confirmation for lead {lead_id} to {lead.correo}.")
    enviar_notificacion(
        destinatario=lead.correo,
        plantilla=plantilla_cliente,
        asunto=asunto_cliente,
        contexto=context,
    )


def procesar_nuevo_agendamiento(appointment_id: int) -> None:
    """Task encolada (transaction.on_commit) al crear un Appointment por el
    booking público. Envía, cada una con dedupe propia:
    1. Confirmación instantánea al cliente: reunión agendada + aviso de que
       la invitación de Google Meet llegará en máx. 24h.
    2. Aviso interno inmediato al equipo (los recordatorios posteriores —
       3d/1d del digest y el aviso de 90 min — ya los cubren los Schedule
       existentes porque el lead queda en REUNION_CONFIRMADA con meeting_at).
    """
    try:
        appointment = Appointment.objects.select_related("lead").get(pk=appointment_id)
    except Appointment.DoesNotExist:
        logger.error(
            f"Appointment {appointment_id} does not exist. Aborting notifications."
        )
        return

    lead = appointment.lead
    horario = presentar(appointment.inicio, appointment.zona_horaria)
    context = {
        "lead": lead,
        "appointment": appointment,
        "nombre": lead.nombre,
        "correo": lead.correo,
        "empresa": lead.empresa,
        "telefono": lead.telefono,
        "mensaje": lead.mensaje or "Sin mensaje adicional.",
        "fecha_hora_visitante": horario["visitante"],
        "zona_horaria": appointment.zona_horaria,
        "fecha_hora_bogota": f"{horario['bogota']} (hora Colombia)",
        "base_url": build_url(""),
    }

    # 1. Confirmación al cliente (instantánea).
    orden_dedupe = f"appointment:{appointment.pk}:confirmacion"
    if reclamar(NotificationLog.Kind.AGENDAMIENTO_CLIENTE, orden_dedupe, lead=lead):
        logger.info(
            "Enviando confirmación de agendamiento %s a %s.",
            appointment.pk,
            lead.correo,
        )
        enviar_notificacion(
            destinatario=lead.correo,
            plantilla="core/emails/agendamiento_confirmado.html",
            asunto="Tu reunión con Sooniverse está agendada",
            contexto=context,
        )

    # 2. Aviso interno inmediato.
    dedupe_interno = f"appointment:{appointment.pk}:aviso-interno"
    if reclamar(NotificationLog.Kind.AGENDAMIENTO_INTERNO, dedupe_interno, lead=lead):
        destinatario_interno = getattr(
            settings, "NOTIFICACION_INTERNA_EMAIL", "soporte@sooniverse.com"
        )
        logger.info(
            "Enviando aviso interno de agendamiento %s a %s.",
            appointment.pk,
            destinatario_interno,
        )
        enviar_notificacion(
            destinatario=destinatario_interno,
            plantilla="core/emails/agendamiento_aviso_interno.html",
            asunto=(
                f"[Nueva Agenda] {lead.nombre} ({lead.correo}) — "
                f"reunión el {horario['bogota']} hora Colombia"
            ),
            contexto=context,
        )


def notificar_diagnostico_completado(questionnaire_id: str) -> None:
    """Task queued when a public questionnaire is submitted (see
    views.public_questionnaire, enqueued via transaction.on_commit).
    Transiciona el lead a 'Diagnóstico realizado' y notifica una sola vez
    (dedupe por questionnaire_id, sobrevive a un doble-submit o a un reintento
    de la tarea)."""
    questionnaire = (
        Questionnaire.objects.select_related("lead").filter(pk=questionnaire_id).first()
    )
    if questionnaire is None:
        logger.error(
            f"Questionnaire {questionnaire_id} does not exist. Aborting notification."
        )
        return

    lead = questionnaire.lead
    if lead.estado == Lead.Estado.DESCARTADO:
        logger.info(
            f"Lead {lead.pk} está Descartado/Spam; se omite notificación de diagnóstico."
        )
        return

    transicionar_lead(
        lead,
        Lead.Estado.DIAGNOSTICO_REALIZADO,
        origen=LeadEstadoHistory.Origen.AUTOMATICO,
        nota=f"Cuestionario {questionnaire.pk} enviado por el cliente.",
    )

    dedupe_key = f"questionnaire:{questionnaire.pk}:completado"
    if not reclamar(NotificationLog.Kind.DIAGNOSTICO_COMPLETADO, dedupe_key, lead=lead):
        return

    enviar_notificacion(
        destinatario=getattr(
            settings, "NOTIFICACION_INTERNA_EMAIL", "soporte@sooniverse.com"
        ),
        plantilla="core/emails/diagnostico_completado.html",
        asunto=f"[Diagnóstico realizado] {lead.empresa}",
        contexto={
            "lead": lead,
            "questionnaire": questionnaire,
            "base_url": build_url(""),
        },
    )


def enviar_digest_diario() -> None:
    """Schedule DAILY (ver sync_schedules) que agrupa en un solo correo:
    leads Nuevo sin atender, reuniones próximas y mantenimientos próximos.
    Reclama todas las dedupe_key y envía dentro de UNA transacción: si el
    envío falla, la excepción revierte los reclamos y el ítem se reintenta
    al día siguiente en vez de quedar marcado como "ya notificado" sin
    haberse enviado."""
    hoy_local = timezone.localdate()
    bloques = construir_digest(hoy_local)

    with transaction.atomic():
        pendientes = {
            nombre: [
                item
                for item in items
                if reclamar(
                    item.kind, item.dedupe_key, lead=item.lead, detalle=item.detalle
                )
            ]
            for nombre, items in bloques.items()
        }
        total = sum(len(v) for v in pendientes.values())
        if total == 0:
            logger.info(f"Digest diario {hoy_local}: nada pendiente.")
            return

        ok = enviar_notificacion(
            destinatario=getattr(
                settings, "NOTIFICACION_INTERNA_EMAIL", "soporte@sooniverse.com"
            ),
            plantilla="core/emails/digest_diario.html",
            asunto=f"[Sooniverse] Resumen diario · {hoy_local:%d/%m/%Y} · {total} pendientes",
            contexto={
                "hoy": hoy_local,
                "base_url": build_url(""),
                "total": total,
                **pendientes,
            },
            fail_silently=False,
        )
        if not ok:
            # No debería ocurrir (fail_silently=False relanza), pero por si
            # enviar_notificacion cambiara de contrato en el futuro.
            raise RuntimeError("Digest diario no pudo enviarse")

    logger.info(f"Digest diario {hoy_local}: {total} ítem(s) notificados.")


def notificar_reuniones_inminentes() -> None:
    """Schedule MINUTES=10 (ver sync_schedules). Barre leads con reunión
    confirmada entre ahora y los próximos 90 minutos y envía un aviso
    puntual — este es el único recordatorio que no cabe en el resumen
    diario. Se usa un barrido periódico en vez de un Schedule ONCE por lead
    para no tener que crear/reprogramar/borrar ese Schedule desde cada punto
    de mutación del lead (ver services/digest.py y el plan para el porqué)."""
    ahora = timezone.now()
    qs = Lead.objects.notificables().filter(
        estado=Lead.Estado.REUNION_CONFIRMADA,
        meeting_at__gte=ahora,
        meeting_at__lte=ahora + timedelta(minutes=90),
    )
    for lead in qs:
        dedupe_key = f"lead:{lead.pk}:reunion:{lead.meeting_at.isoformat()}:90m"
        with transaction.atomic():
            if not reclamar(
                NotificationLog.Kind.REUNION_INMINENTE, dedupe_key, lead=lead
            ):
                continue
            enviar_notificacion(
                destinatario=getattr(
                    settings, "NOTIFICACION_INTERNA_EMAIL", "soporte@sooniverse.com"
                ),
                plantilla="core/emails/reunion_inminente.html",
                asunto=f"[Reunión en 90 min] {lead.empresa}",
                contexto={
                    "lead": lead,
                    "base_url": build_url(""),
                    "meeting_local": timezone.localtime(lead.meeting_at),
                },
                fail_silently=False,
            )

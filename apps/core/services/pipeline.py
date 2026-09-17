"""Punto único de mutación de estado para Lead.

transicionar_lead() es el único lugar que debe cambiar Lead.estado. Lo usan
la vista lead_update_status, la tarea que reacciona al cuestionario
completado, y (opcionalmente) el admin/formularios internos. Centralizarlo
aquí es lo que hace confiable estado_actualizado_en, que a su vez es el
ancla del recordatorio de 7 días para leads en estado Nuevo.
"""
import logging

from django.utils import timezone

from ..models import Lead, LeadEstadoHistory

logger = logging.getLogger("django.apps.core.pipeline")


def transicionar_lead(
    lead: Lead,
    nuevo_estado: str,
    *,
    usuario=None,
    origen: str = LeadEstadoHistory.Origen.MANUAL,
    nota: str = "",
) -> bool:
    """Cambia lead.estado a nuevo_estado, registra el historial y actualiza
    estado_actualizado_en. Devuelve False (no-op) si el estado no cambia."""
    estado_anterior = lead.estado
    if estado_anterior == nuevo_estado:
        logger.info(
            "Lead %s ya está en estado %s; transición ignorada (no-op).",
            lead.pk,
            nuevo_estado,
        )
        return False

    ahora = timezone.now()
    lead.estado = nuevo_estado
    lead.estado_actualizado_en = ahora
    lead.save(update_fields=["estado", "estado_actualizado_en", "actualizado_en"])

    LeadEstadoHistory.objects.create(
        lead=lead,
        estado_anterior=estado_anterior,
        estado_nuevo=nuevo_estado,
        cambiado_por=usuario,
        origen=origen,
        nota=nota,
    )
    logger.info(
        "Lead %s transicionado de %s a %s (origen=%s).",
        lead.pk,
        estado_anterior,
        nuevo_estado,
        origen,
    )
    return True

"""Construcción del contenido del resumen diario del CRM.

Todas las comparaciones de "N días antes"/"N días sin atender" son de DÍA
CALENDARIO en hora local (America/Bogota, ver settings.TIME_ZONE), nunca
aritmética de timedelta sobre datetimes en UTC — el resumen es un correo de
una vez al día, así que "3 días antes" debe significar diferencia de fecha
en Bogotá, o una reunión a las 06:00 y otra a las 22:00 del mismo día
caerían en cubos distintos.

Este módulo solo LEE y arma los ítems candidatos; la tarea que lo llama
(apps.core.tasks.enviar_digest_diario) es responsable de reclamar cada
dedupe_key con apps.core.services.dedupe.reclamar() antes de enviar, dentro
de una única transacción con el envío del correo.
"""
from dataclasses import dataclass, field
from datetime import date, timedelta

from django.db.models.functions import Coalesce
from django.utils import timezone

from ..models import Lead, MaintenanceWindow, NotificationLog


@dataclass
class ItemDigest:
    kind: str
    dedupe_key: str
    lead: Lead
    titulo: str
    detalle: dict = field(default_factory=dict)


def _leads_nuevos_sin_atender(hoy_local: date) -> list[ItemDigest]:
    """Leads en estado Nuevo, desde el día siguiente a su llegada (el día 0
    ya tuvo su correo instantáneo) y hasta 7 días después. Pasado ese
    umbral simplemente dejan de aparecer aquí — no hay bandera que
    "desactivar", el corte es el propio filtro de fecha."""
    limite = timezone.now() - timedelta(days=7)
    qs = (
        Lead.objects.notificables()
        .filter(estado=Lead.Estado.NUEVO)
        .annotate(entro_en=Coalesce("estado_actualizado_en", "creado_en"))
        .filter(entro_en__gte=limite)
    )
    items = []
    for lead in qs:
        entro_en_local = timezone.localtime(lead.entro_en).date()
        dias = (hoy_local - entro_en_local).days
        if dias < 1:
            continue
        items.append(
            ItemDigest(
                kind=NotificationLog.Kind.LEAD_NUEVO_RECORDATORIO,
                dedupe_key=f"lead:{lead.pk}:nuevo:{hoy_local.isoformat()}",
                lead=lead,
                titulo=f"{lead.empresa} — {dias} día(s) sin atender",
                detalle={"dias": dias},
            )
        )
    return items


def _reuniones_proximas(hoy_local: date) -> list[ItemDigest]:
    """Reuniones confirmadas a 3 o 1 día(s) de distancia (día calendario)."""
    qs = Lead.objects.notificables().filter(
        estado=Lead.Estado.REUNION_CONFIRMADA, meeting_at__isnull=False
    )
    items = []
    for lead in qs:
        meeting_local = timezone.localtime(lead.meeting_at)
        dias = (meeting_local.date() - hoy_local).days
        if dias not in (3, 1):
            continue
        items.append(
            ItemDigest(
                kind=NotificationLog.Kind.REUNION_RECORDATORIO,
                dedupe_key=f"lead:{lead.pk}:reunion:{lead.meeting_at.isoformat()}:{dias}d",
                lead=lead,
                titulo=f"{lead.empresa} — reunión en {dias} día(s) ({meeting_local:%d/%m %H:%M})",
                detalle={"dias": dias, "meeting_at": lead.meeting_at.isoformat()},
            )
        )
    return items


def _mantenimientos_proximos(hoy_local: date) -> list[ItemDigest]:
    """Ventanas de mantenimiento a 15, 7, 3 o 0 días. No se condiciona a que
    el lead siga en estado 'Mantenimiento programado': la ventana es un
    compromiso independiente de esa etiqueta, y condicionarlo dejaría caer
    avisos en silencio si el operador mueve el lead a otro estado. Solo
    completed=True y Descartado/Spam la suprimen."""
    qs = (
        MaintenanceWindow.objects.filter(completed=False)
        .exclude(lead__estado=Lead.Estado.DESCARTADO)
        .select_related("lead")
    )
    items = []
    for mw in qs:
        scheduled_local = timezone.localtime(mw.scheduled_for)
        dias = (scheduled_local.date() - hoy_local).days
        if dias not in (15, 7, 3, 0):
            continue
        items.append(
            ItemDigest(
                kind=NotificationLog.Kind.MANTENIMIENTO_RECORDATORIO,
                dedupe_key=f"mw:{mw.pk}:{mw.scheduled_for.isoformat()}:{dias}d",
                lead=mw.lead,
                titulo=(
                    f"{mw.lead.empresa} — mantenimiento "
                    f"{'hoy' if dias == 0 else f'en {dias} día(s)'} "
                    f"({scheduled_local:%d/%m %H:%M})"
                ),
                detalle={"dias": dias, "scheduled_for": mw.scheduled_for.isoformat(), "window_id": mw.pk},
            )
        )
    return items


def construir_digest(hoy_local: date) -> dict[str, list[ItemDigest]]:
    return {
        "leads_nuevos": _leads_nuevos_sin_atender(hoy_local),
        "reuniones": _reuniones_proximas(hoy_local),
        "mantenimientos": _mantenimientos_proximos(hoy_local),
    }

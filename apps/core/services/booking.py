"""Motor de disponibilidad del booking público (/agendar/).

Los horarios del negocio (DiaHorario) viven en America/Bogota
(settings.TIME_ZONE): 9-18 significa "9-18 hora Colombia". El visitante
elige su propia zona horaria (IANA, p. ej. America/Mexico_City) y este
módulo hace la conversión con zoneinfo: un slot existe en un instante UTC
concreto y cada cliente lo ve en su fecha/hora local.

Por eso, para responder "?qué slots hay el 2026-10-05 (fecha DEL VISITANTE)?"
se generan los slots de los días de negocio candidatos (fecha-1, fecha y
fecha+1 en Bogotá — suficiente porque los desplazamientos máximos de huso
son ~±14h) y se conservan los que caen en esa fecha una vez convertida a la
zona horaria del visitante.
"""

import logging
from datetime import datetime, timedelta
from datetime import timezone as dt_timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from django.conf import settings
from django.utils import timezone

from ..models import Appointment, BookingConfig, DiaHorario

logger = logging.getLogger("django.apps.core.booking")

# Fallback si el visitante envía una zona horaria desconocida.
ZONA_FALLBACK = getattr(settings, "TIME_ZONE", "America/Bogota")


def zona_segura(tz_name: str | None) -> str:
    """Valida un nombre IANA de zona horaria; devuelve Colombia si es None,
    vacío o desconocido (protege contra input arbitrario en la API)."""
    if not tz_name:
        return ZONA_FALLBACK
    try:
        ZoneInfo(tz_name)
    except (ZoneInfoNotFoundError, ValueError, KeyError):
        return ZONA_FALLBACK
    return tz_name


def _horarios_por_dia() -> dict[int, tuple]:
    """{weekday: (inicio, fin)} con los DiaHorario activos. El .weekday() de
    Python es 0=Lunes...6=Domingo, igual que DiaHorario.dia."""
    return {
        h.dia: (h.hora_inicio, h.hora_fin)
        for h in DiaHorario.objects.filter(activo=True)
    }


def _generar_slots_dia_negocio(fecha_bogota, config) -> list[datetime]:
    """Slots UTC de UN día de negocio — la fecha es la del calendario de
    Bogotá, y el horario semanal se mira por su weekday. Slots cada
    duracion_min, sin solapestos (el paso avanza en la misma duración)."""
    cfg = _horarios_por_dia().get(fecha_bogota.weekday())
    if cfg is None:
        return []

    inicio_cfg, fin_cfg = cfg
    tz_bogota = ZoneInfo(settings.TIME_ZONE)
    paso = timedelta(minutes=config.duracion_min)

    cursor = datetime.combine(fecha_bogota, inicio_cfg, tzinfo=tz_bogota)
    limite = datetime.combine(fecha_bogota, fin_cfg, tzinfo=tz_bogota)

    slots = []
    while cursor + paso <= limite:
        # Colombia nunca observa DST; timezone.make_aware también serviría,
        # pero el aware explícito es inequívoco (sin fold/ambigüedad).
        slots.append(cursor.astimezone(dt_timezone.utc))
        cursor += paso
    return slots


def _inicios_confirmados(desde: datetime, hasta: datetime) -> list[datetime]:
    rows = Appointment.objects.filter(
        estado=Appointment.Estado.CONFIRMADA,
        inicio__gte=desde,
        inicio__lt=hasta,
    ).values_list("inicio", flat=True)
    return list(rows)


def _pertenece_a_ventana(slot: datetime, config, hoy_bogota) -> bool:
    dia = timezone.localtime(slot).date()
    delta = (dia - hoy_bogota).days
    return 0 <= delta <= config.dias_apertura


def slots_para_fecha(fecha_iso: str, tz_name: str | None) -> dict:
    """Slots visibles para una fecha dada EN LA ZONA HORARIA DEL VISITANTE.

    Devuelve {"fecha": iso, "zona_horaria": tz_validada, "slots": [iso_utc]}
    ordenado cronológicamente. El frontend formatea cada instante UTC con la
    tz elegida en formato 24h; por eso un slot de la noche de Bogotá puede
    aparecer en el día siguiente del visitante (y viceversa).
    """
    config = BookingConfig.get_solo()
    tz_valida = zona_segura(tz_name)
    tz_visitante = ZoneInfo(tz_valida)
    tz_bogota = ZoneInfo(settings.TIME_ZONE)

    try:
        # Solo se usa .date(); el tzinfo es irrelevante aquí. noqa: DTZ007
        fecha_visitante = datetime.strptime(fecha_iso, "%Y-%m-%d").date()  # noqa: DTZ007
    except (ValueError, TypeError):
        return {"fecha": fecha_iso, "zona_horaria": tz_valida, "slots": []}

    ahora = timezone.now()
    limite_reserva = ahora + timedelta(minutes=config.anticipo_min)
    hoy_bogota = ahora.astimezone(tz_bogota).date()

    candidatos: list[datetime] = []
    for delta in (-1, 0, 1):
        dia_bogota = fecha_visitante + timedelta(days=delta)
        for slot_utc in _generar_slots_dia_negocio(dia_bogota, config):
            if slot_utc < limite_reserva:
                continue
            if not _pertenece_a_ventana(slot_utc, config, hoy_bogota):
                continue
            if slot_utc.astimezone(tz_visitante).date() != fecha_visitante:
                continue
            candidatos.append(slot_utc)
    candidatos = sorted(candidatos)
    if not candidatos:
        return {
            "fecha": fecha_visitante.isoformat(),
            "zona_horaria": tz_valida,
            "slots": [],
        }

    # Un único query de ocupación cubre todo el rango consultado; el
    # traslape se evalúa en memoria (host único: una cita ocupa su rango
    # completo, no solo el instante de inicio).
    ocupados = _inicios_confirmados(
        candidatos[0] - timedelta(minutes=config.duracion_min),
        candidatos[-1] + timedelta(minutes=config.duracion_min),
    )
    pasos = timedelta(minutes=config.duracion_min).total_seconds()
    libres = [
        s
        for s in candidatos
        if not any(abs((o - s).total_seconds()) < pasos for o in ocupados)
    ]

    return {
        "fecha": fecha_visitante.isoformat(),
        "zona_horaria": tz_valida,
        "slots": [s.isoformat() for s in libres],
    }


def fechas_disponibles(tz_name: str | None) -> list[str]:
    """Próximas fechas (en la zona horaria del visitante) con al menos un
    slot reservable dentro de la ventana de apertura. Orden cronológico."""
    config = BookingConfig.get_solo()
    tz_valida = zona_segura(tz_name)
    tz_visitante = ZoneInfo(tz_valida)
    tz_bogota = ZoneInfo(settings.TIME_ZONE)

    ahora = timezone.now()
    limite_reserva = ahora + timedelta(minutes=config.anticipo_min)
    hoy_bogota = ahora.astimezone(tz_bogota).date()
    hoy_visitante = ahora.astimezone(tz_visitante).date()

    # Genera el catálogo completo de slots de la ventana una sola vez
    # (dias_apertura + 1 días de negocio en Bogotá, más un día de margen para
    # husos desplazados) y agrupa por fecha local del visitante.
    catalogo: dict = {}
    for delta in range(-1, config.dias_apertura + 2):
        dia_bogota = hoy_bogota + timedelta(days=delta)
        for slot_utc in _generar_slots_dia_negocio(dia_bogota, config):
            if slot_utc < limite_reserva:
                continue
            if not _pertenece_a_ventana(slot_utc, config, hoy_bogota):
                continue
            catalogo.setdefault(slot_utc.astimezone(tz_visitante).date(), []).append(
                slot_utc
            )

    if not catalogo:
        return []

    todas = sorted(s for slots in catalogo.values() for s in slots)
    ocupados = _inicios_confirmados(
        todas[0] - timedelta(minutes=config.duracion_min),
        todas[-1] + timedelta(minutes=config.duracion_min),
    )
    pasos = timedelta(minutes=config.duracion_min).total_seconds()

    fechas = []
    for delta in range(config.dias_apertura + 1):
        fecha = hoy_visitante + timedelta(days=delta)
        slots = catalogo.get(fecha, [])
        # Ojo: un slot "libre" aquí es referencial (rápido, para decidir qué
        # fechas mostrar); la validez exacta se re-ejecuta en validar_slot().
        libres = [
            s
            for s in slots
            if not any(abs((o - s).total_seconds()) < pasos for o in ocupados)
        ]
        if libres:
            fechas.append(fecha.isoformat())
    return fechas


def validar_slot(inicio_utc: datetime) -> tuple[bool, str]:
    """Re-validación server-side al reservar: ventana de apertura, horario
    semanal en Bogotá, antelación mínima y disponibilidad (traslape con otra
    cita confirmada). Devuelve (ok, motivo)."""
    config = BookingConfig.get_solo()
    if timezone.is_naive(inicio_utc):
        return False, "slot-naive"

    ahora = timezone.now()
    if inicio_utc < ahora:
        return False, "slot-pasado"
    if inicio_utc < ahora + timedelta(minutes=config.anticipo_min):
        return False, "anticipo-insuficiente"

    tz_bogota = ZoneInfo(settings.TIME_ZONE)
    hoy_bogota = ahora.astimezone(tz_bogota).date()
    dia_bogota = inicio_utc.astimezone(tz_bogota).date()
    if (dia_bogota - hoy_bogota).days > config.dias_apertura:
        return False, "fuera-de-ventana"

    # Debe corresponder EXACTAMENTE a un slot del horario semanal (evita
    # type-in de fechas manuales contra la API).
    if inicio_utc not in _generar_slots_dia_negocio(dia_bogota, config):
        return False, "slot-invalido"

    fin = inicio_utc + timedelta(minutes=config.duracion_min)
    conflicto = Appointment.objects.filter(
        estado=Appointment.Estado.CONFIRMADA,
        inicio__lt=fin,
        inicio__gt=inicio_utc - timedelta(minutes=config.duracion_min),
    ).exists()
    if conflicto:
        return False, "slot-ocupado"
    return True, "ok"


def presentar(inicio_utc: datetime, tz_name: str) -> dict:
    """Representaciones legibles para correos/CRM: hora Colombia y la zona
    elegida por el visitante, ambas 24h."""
    local = timezone.localtime(inicio_utc)
    visitante = inicio_utc.astimezone(ZoneInfo(zona_segura(tz_name)))
    return {
        "bogota": local.strftime("%d/%m/%Y %H:%M"),
        "visitante": visitante.strftime("%d/%m/%Y %H:%M"),
        "zona_horaria": tz_name,
    }

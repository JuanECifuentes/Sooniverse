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

from ..models import Appointment, BookingConfig, DiaHorario, Lead

logger = logging.getLogger("django.apps.core.booking")

# Fallback si el visitante envía una zona horaria desconocida.
ZONA_FALLBACK = getattr(settings, "TIME_ZONE", "America/Bogota")
DESCANSO_MIN = 20
ANTICIPO_MINIMO_MIN = 1440  # Mínimo 24 horas (1440 minutos)


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


def _citas_confirmadas_rango(
    desde: datetime, hasta: datetime
) -> list[tuple[datetime, datetime]]:
    """Obtiene intervalos (inicio, fin) en UTC de citas confirmadas y reuniones agendadas."""
    citas = []
    # 1. Appointments confirmados
    for apt in Appointment.objects.filter(
        estado=Appointment.Estado.CONFIRMADA,
        inicio__lt=hasta,
        fin__gt=desde,
    ).values("inicio", "fin", "duracion_min"):
        ini = apt["inicio"]
        fin = apt["fin"] or (ini + timedelta(minutes=apt["duracion_min"] or 30))
        citas.append((ini, fin))

    # 2. Leads con meeting_at que no tengan ya Appointment confirmado asociado
    leads_reunion = (
        Lead.objects.filter(
            meeting_at__isnull=False,
            meeting_at__gte=desde - timedelta(hours=2),
            meeting_at__lt=hasta,
        )
        .exclude(appointments__estado=Appointment.Estado.CONFIRMADA)
        .values_list("meeting_at", flat=True)
    )
    for m_at in leads_reunion:
        citas.append((m_at, m_at + timedelta(minutes=30)))

    if not citas:
        return []
    citas.sort(key=lambda x: x[0])
    return citas


def _generar_slots_dia_negocio(
    fecha_bogota,
    config,
    citas_precargadas: list[tuple[datetime, datetime]] | None = None,
) -> list[datetime]:
    """Genera los slots UTC disponibles para un día de negocio en Bogotá.

    Aplica una redistribución dinámica cuando hay citas confirmadas:
    - Se garantiza un margen de descanso de DESCANSO_MIN (20 min) antes y después de cada reunión.
    - Si se agenda una reunión (ej. a las 10:30), los horarios posteriores se redistribuyen
      arrancando exactamente en fin_cita + 20min (ej. 11:20) avanzando con paso duracion + descanso (50min).
    - Los horarios previos se ajustan respetando el límite de apertura y el margen previo a la cita (ej. 09:00, 09:40).
    """
    cfg = _horarios_por_dia().get(fecha_bogota.weekday())
    if cfg is None:
        return []

    inicio_cfg, fin_cfg = cfg
    tz_bogota = ZoneInfo(settings.TIME_ZONE)
    duracion = timedelta(minutes=config.duracion_min)
    descanso = timedelta(minutes=DESCANSO_MIN)
    step = duracion + descanso

    limite_inicio = datetime.combine(
        fecha_bogota, inicio_cfg, tzinfo=tz_bogota
    ).astimezone(dt_timezone.utc)
    limite_fin = datetime.combine(
        fecha_bogota, fin_cfg, tzinfo=tz_bogota
    ).astimezone(dt_timezone.utc)

    if citas_precargadas is not None:
        citas_dia = [
            (c_ini, c_fin)
            for c_ini, c_fin in citas_precargadas
            if c_ini < limite_fin and c_fin > limite_inicio
        ]
    else:
        citas_dia = _citas_confirmadas_rango(limite_inicio, limite_fin)

    # Si no hay ninguna cita confirmada en el día, slots estándar cada duracion_min
    if not citas_dia:
        slots = []
        cursor = limite_inicio
        while cursor + duracion <= limite_fin:
            slots.append(cursor)
            cursor += duracion
        return slots

    # Fusionar citas que se solapan o están a menos del margen de descanso
    citas_merged = []
    for c_start, c_end in citas_dia:
        if not citas_merged:
            citas_merged.append([c_start, c_end])
        else:
            prev = citas_merged[-1]
            if c_start <= prev[1] + descanso:
                prev[1] = max(prev[1], c_end)
            else:
                citas_merged.append([c_start, c_end])

    # Construir ventanas libres de la jornada
    ventanas = []
    primera = citas_merged[0]
    if limite_inicio < primera[0] - descanso:
        ventanas.append((limite_inicio, primera[0] - descanso, "antes"))

    for i in range(len(citas_merged) - 1):
        c_act = citas_merged[i]
        c_sig = citas_merged[i + 1]
        w_ini = c_act[1] + descanso
        w_fin = c_sig[0] - descanso
        if w_ini < w_fin:
            ventanas.append((w_ini, w_fin, "intermedia"))

    ultima = citas_merged[-1]
    if ultima[1] + descanso < limite_fin:
        ventanas.append((ultima[1] + descanso, limite_fin, "despues"))

    slots_set = set()
    for w_ini, w_fin, tipo in ventanas:
        if w_fin - w_ini < duracion:
            continue

        if tipo == "antes":
            # Hacia adelante desde el inicio del día
            cursor = w_ini
            while cursor + duracion <= w_fin:
                slots_set.add(cursor)
                cursor += step
            # Alinear también hacia atrás desde el límite previo a la cita (ej. 09:40 si cita es 10:30)
            slot_backward = w_fin - duracion
            if slot_backward >= w_ini:
                slots_set.add(slot_backward)
        else:
            # Hacia adelante desde fin_reunion + descanso (ej. 11:20, 12:10, 13:00...)
            cursor = w_ini
            while cursor + duracion <= w_fin:
                slots_set.add(cursor)
                cursor += step

    return sorted(slots_set)


def _pertenece_a_ventana(slot: datetime, config, hoy_bogota) -> bool:
    dia = timezone.localtime(slot).date()
    delta = (dia - hoy_bogota).days
    return 0 <= delta <= config.dias_apertura


def slots_para_fecha(fecha_iso: str, tz_name: str | None) -> dict:
    """Slots visibles para una fecha dada EN LA ZONA HORARIA DEL VISITANTE.

    Devuelve {"fecha": iso, "zona_horaria": tz_validada, "slots": [iso_utc]}
    ordenado cronológicamente. El frontend formatea cada instante UTC con la
    tz elegida en formato 24h.
    """
    config = BookingConfig.get_solo()
    tz_valida = zona_segura(tz_name)
    tz_visitante = ZoneInfo(tz_valida)
    tz_bogota = ZoneInfo(settings.TIME_ZONE)

    try:
        fecha_visitante = datetime.strptime(fecha_iso, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return {"fecha": fecha_iso, "zona_horaria": tz_valida, "slots": []}

    ahora = timezone.now()
    anticipo_minimo = max(config.anticipo_min, ANTICIPO_MINIMO_MIN)
    limite_reserva = ahora + timedelta(minutes=anticipo_minimo)
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

    duracion = timedelta(minutes=config.duracion_min)
    descanso = timedelta(minutes=DESCANSO_MIN)
    citas = _citas_confirmadas_rango(
        candidatos[0] - timedelta(hours=2),
        candidatos[-1] + timedelta(hours=2),
    )
    libres = [
        s
        for s in candidatos
        if not any(
            (s < c_end + descanso and s + duracion + descanso > c_start)
            for c_start, c_end in citas
        )
    ]

    return {
        "fecha": fecha_visitante.isoformat(),
        "zona_horaria": tz_valida,
        "slots": [s.isoformat() for s in libres],
    }


def disponibilidad_completa_ventana(tz_name: str | None) -> dict:
    """Calcula y devuelve las fechas disponibles y los slots libres de cada una en
    la zona horaria del visitante para toda la ventana de agenda abierta.
    """
    config = BookingConfig.get_solo()
    tz_valida = zona_segura(tz_name)
    tz_visitante = ZoneInfo(tz_valida)
    tz_bogota = ZoneInfo(settings.TIME_ZONE)

    ahora = timezone.now()
    anticipo_minimo = max(config.anticipo_min, ANTICIPO_MINIMO_MIN)
    limite_reserva = ahora + timedelta(minutes=anticipo_minimo)
    hoy_bogota = ahora.astimezone(tz_bogota).date()
    hoy_visitante = ahora.astimezone(tz_visitante).date()

    limite_inicio_ventana = datetime.combine(
        hoy_bogota - timedelta(days=1), datetime.min.time(), tzinfo=tz_bogota
    ).astimezone(dt_timezone.utc)
    limite_fin_ventana = datetime.combine(
        hoy_bogota + timedelta(days=config.dias_apertura + 2),
        datetime.max.time(),
        tzinfo=tz_bogota,
    ).astimezone(dt_timezone.utc)
    citas_ventana = _citas_confirmadas_rango(limite_inicio_ventana, limite_fin_ventana)

    catalogo: dict = {}
    for delta in range(-1, config.dias_apertura + 2):
        dia_bogota = hoy_bogota + timedelta(days=delta)
        for slot_utc in _generar_slots_dia_negocio(
            dia_bogota, config, citas_precargadas=citas_ventana
        ):
            if slot_utc < limite_reserva:
                continue
            if not _pertenece_a_ventana(slot_utc, config, hoy_bogota):
                continue
            catalogo.setdefault(slot_utc.astimezone(tz_visitante).date(), []).append(
                slot_utc
            )

    if not catalogo:
        return {
            "zona_horaria": tz_valida,
            "fechas_disponibles": [],
            "slots_por_fecha": {},
        }

    duracion = timedelta(minutes=config.duracion_min)
    descanso = timedelta(minutes=DESCANSO_MIN)

    fechas = []
    slots_por_fecha = {}
    for delta in range(config.dias_apertura + 1):
        fecha = hoy_visitante + timedelta(days=delta)
        slots = catalogo.get(fecha, [])
        libres = [
            s
            for s in slots
            if not any(
                (s < c_end + descanso and s + duracion + descanso > c_start)
                for c_start, c_end in citas_ventana
            )
        ]
        if libres:
            fecha_iso = fecha.isoformat()
            fechas.append(fecha_iso)
            slots_por_fecha[fecha_iso] = [s.isoformat() for s in sorted(libres)]

    return {
        "zona_horaria": tz_valida,
        "fechas_disponibles": fechas,
        "slots_por_fecha": slots_por_fecha,
    }


def fechas_disponibles(tz_name: str | None) -> list[str]:
    """Próximas fechas (en la zona horaria del visitante) con al menos un
    slot reservable dentro de la ventana de apertura. Orden cronológico."""
    return disponibilidad_completa_ventana(tz_name)["fechas_disponibles"]


def validar_slot(inicio_utc: datetime) -> tuple[bool, str]:
    """Re-validación server-side al reservar: ventana de apertura, horario
    semanal en Bogotá, antelación mínima (>= 24hr), correspondencia con slots
    redistribuidos y verificación del margen de descanso de 20 minutos. Devuelve (ok, motivo)."""
    config = BookingConfig.get_solo()
    if timezone.is_naive(inicio_utc):
        return False, "slot-naive"

    ahora = timezone.now()
    if inicio_utc < ahora:
        return False, "slot-pasado"

    # Mínimo 24 horas (1440 min)
    anticipo_minimo = max(config.anticipo_min, ANTICIPO_MINIMO_MIN)
    if inicio_utc < ahora + timedelta(minutes=anticipo_minimo):
        return False, "anticipo-insuficiente"

    tz_bogota = ZoneInfo(settings.TIME_ZONE)
    hoy_bogota = ahora.astimezone(tz_bogota).date()
    dia_bogota = inicio_utc.astimezone(tz_bogota).date()
    if (dia_bogota - hoy_bogota).days > config.dias_apertura:
        return False, "fuera-de-ventana"

    # Verificar que el slot pertenezca a los slots válidos redistribuidos del día
    slots_validos = _generar_slots_dia_negocio(dia_bogota, config)
    if inicio_utc not in slots_validos:
        return False, "slot-invalido"

    # Verificar que no colisione con citas confirmadas ni viole el descanso de 20 min
    duracion = timedelta(minutes=config.duracion_min)
    descanso = timedelta(minutes=DESCANSO_MIN)
    citas = _citas_confirmadas_rango(
        inicio_utc - timedelta(hours=2),
        inicio_utc + timedelta(hours=2),
    )
    for c_start, c_end in citas:
        if inicio_utc < c_end + descanso and inicio_utc + duracion + descanso > c_start:
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

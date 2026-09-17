"""Vistas públicas del booking (/agendar/).

Mismo esquema de protección que contacto_lead (rate limit por IP, honeypot,
reCAPTCHA v3) pero con acción recaptcha propia ("agenda_booking") y listo
más estricto: SI un endpoint no recibe token válido no toca la BD. La
detección de país/zona horaria por IP se hace EN EL NAVEGADOR (ipapi.co)
— estos endpoints solo reciben la zona horaria ya elegida/detectada.
"""

import datetime
import json
import logging
import re

from django.conf import settings
from django.core.cache import cache
from django.db import IntegrityError, transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.http import require_GET, require_http_methods
from django_q.tasks import async_task

from .models import Appointment, BookingConfig, Lead, LeadEstadoHistory
from .recaptcha import verify_recaptcha
from .services import booking as svc
from .services.pipeline import transicionar_lead

logger = logging.getLogger("django.apps.core.views_booking")

# Acción recaptcha exclusiva del flujo de agenda.
RECAPTCHA_ACTION_BOOKING = "agenda_booking"

ZONA_NEGOCIO = settings.TIME_ZONE  # America/Bogota — referencia del negocio

RE_PREFIJO = re.compile(r"^\+\d{1,4}$")
RE_TELEFONO = re.compile(r"^\d{6,15}$")
RE_CORREO = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

MENSAJES_SLOT = {
    "slot-pasado": "El horario elegido ya pasó. Selecciona otro horario.",
    "anticipo-insuficiente": "Debes agendar con la antelación mínima configurada. Elige otro horario.",
    "fuera-de-ventana": "La fecha elegida queda fuera de la ventana de agenda abierta.",
    "slot-invalido": "El horario elegido no está disponible. Actualiza y elige otro.",
    "slot-ocupado": "Alguien acaba de tomar ese horario. Elige otro, por favor.",
    "slot-naive": "Petición inválida.",
}


def get_client_ip(request) -> str:
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")


def _rate_limit_ok(ip: str) -> bool:
    """Rate limit por IP con clave propia del booking (una sesión legítima
    hace varios GET de disponibilidad mientras el usuario explora fechas,
    así que es más generoso que el límite del formulario de contacto)."""
    limit = getattr(settings, "BOOKING_RATE_LIMIT_LIMIT", 30)
    window = getattr(settings, "BOOKING_RATE_LIMIT_WINDOW", 600)
    key = f"rate_limit_booking_{ip}"
    current = cache.get(key, 0)
    if current >= limit:
        logger.warning("Booking rate limit excedido para IP %s", ip)
        return False
    cache.set(key, current + 1, timeout=window)
    return True


@require_GET
def booking_publico(request):
    """Página pública de agendamiento (2 pasos)."""
    return render(
        request,
        "core/booking/agendar.html",
        {
            "config": BookingConfig.get_solo(),
            "zona_negocio": ZONA_NEGOCIO,
            "recaptcha_action": RECAPTCHA_ACTION_BOOKING,
        },
    )


@require_GET
def booking_disponibilidad(request):
    """GET /agendar/api/disponibilidad/?tz=<IANA>&fecha=<YYYY-MM-DD>

    Devuelve fechas con disponibilidad + slots de la fecha pedida (en la
    zona del visitante). Protegido: reCAPTCHA + rate limit — sin token
    válido responde 403 sin tocar la BD.
    """
    ip = get_client_ip(request)
    if not _rate_limit_ok(ip):
        return JsonResponse(
            {
                "success": False,
                "message": "Demasiadas solicitudes. Intente nuevamente más tarde.",
            },
            status=429,
        )

    ok, reason = verify_recaptcha(
        request.GET.get("g-recaptcha-response", ""),
        remote_ip=ip,
        expected_action=RECAPTCHA_ACTION_BOOKING,
    )
    if not ok:
        logger.warning("reCAPTCHA rechazado (disponibilidad) IP %s (%s).", ip, reason)
        return JsonResponse(
            {
                "success": False,
                "message": "No fue posible validar la seguridad de la solicitud.",
            },
            status=403,
        )

    tz_name = request.GET.get("tz")
    fecha = request.GET.get("fecha")
    config = BookingConfig.get_solo()
    tz_valida = svc.zona_segura(tz_name)

    fechas = svc.fechas_disponibles(tz_valida)
    slots = svc.slots_para_fecha(fecha or (fechas[0] if fechas else ""), tz_valida)

    return JsonResponse(
        {
            "success": True,
            "zona_horaria": slots["zona_horaria"],
            "zona_negocio": ZONA_NEGOCIO,
            "duracion_min": config.duracion_min,
            "dias_apertura": config.dias_apertura,
            "fechas_disponibles": fechas,
            "fecha": slots["fecha"],
            "slots": slots["slots"],
        }
    )


@require_http_methods(["POST"])
def booking_reservar(request):
    """POST /agendar/api/reservar/ — JSON:
    {inicio, zona_horaria, nombre, correo, telefono_prefijo, telefono_numero,
     empresa?, mensaje?, consentimiento, website_verification (honeypot),
     g-recaptcha-response}

    Efectos: Lead (nuevo o existente) + Appointment + lead -> estado
    REUNION_CONFIRMADA con meeting_at (sin link de Meet) + correos.
    """
    ip = get_client_ip(request)
    if not _rate_limit_ok(ip):
        return JsonResponse(
            {"success": False, "message": "Demasiadas solicitudes. Intente más tarde."},
            status=429,
        )

    try:
        data = json.loads(request.body or "{}")
    except (json.JSONDecodeError, TypeError):
        return JsonResponse({"success": False, "message": "JSON inválido."}, status=400)

    # Honeypot — los bots lo llenan.
    if data.get("website_verification"):
        logger.warning("Honeypot activado desde IP %s (booking).", ip)
        return JsonResponse(
            {"success": False, "message": "Petición rechazada."}, status=400
        )

    ok, reason = verify_recaptcha(
        data.get("g-recaptcha-response", ""),
        remote_ip=ip,
        expected_action=RECAPTCHA_ACTION_BOOKING,
    )
    if not ok:
        logger.warning("reCAPTCHA rechazado (reserva) IP %s (%s).", ip, reason)
        return JsonResponse(
            {
                "success": False,
                "message": "No fue posible validar la seguridad de la solicitud. Recargue la página e intente nuevamente.",
            },
            status=403,
        )

    # Consentimiento obligatorio.
    if data.get("consentimiento") is not True:
        return JsonResponse(
            {
                "success": False,
                "message": "Debes confirmar el consentimiento de contacto para agendar.",
            },
            status=400,
        )

    nombre = str(data.get("nombre", "") or "").strip()
    correo = str(data.get("correo", "") or "").strip()
    prefijo = str(data.get("telefono_prefijo", "") or "").strip()
    numero = str(data.get("telefono_numero", "") or "").strip()
    empresa = str(data.get("empresa", "") or "").strip()[:255]
    mensaje = str(data.get("mensaje", "") or "").strip()

    errores = []
    if not nombre or len(nombre) > 255:
        errores.append("El nombre completo es obligatorio.")
    if not RE_CORREO.match(correo):
        errores.append("El correo electrónico no es válido.")
    if not RE_PREFIJO.match(prefijo):
        errores.append("El prefijo telefónico es inválido.")
    if not RE_TELEFONO.match(numero):
        errores.append("El número de teléfono es inválido (6-15 dígitos).")
    if errores:
        return JsonResponse(
            {"success": False, "message": " ".join(errores)}, status=400
        )

    # Máx. 2 agendamientos futuros por el mismo correo — bloquea el llenado
    # de la agenda por automatización de ataque.
    futuras = Appointment.objects.filter(
        estado=Appointment.Estado.CONFIRMADA,
        inicio__gt=timezone.now(),
        lead__correo__iexact=correo,
    ).count()
    if futuras >= 2:
        logger.warning(
            "Límite de 2 futuras al correo %s alcanzado (IP %s).", correo, ip
        )
        return JsonResponse(
            {
                "success": False,
                "message": "Ya existen 2 reuniones futuras agendadas con este correo. Para cambiar el horario, escríbenos antes de crear una nueva reserva.",
            },
            status=429,
        )

    # Parse del slot: ISO con offset obligatorio (aware).
    try:
        inicio = datetime.datetime.fromisoformat(str(data.get("inicio", "")))
    except (ValueError, TypeError):
        return JsonResponse(
            {"success": False, "message": "Fecha/hora inválida."}, status=400
        )
    if timezone.is_naive(inicio):
        return JsonResponse(
            {"success": False, "message": MENSAJES_SLOT["slot-naive"]}, status=400
        )

    config = BookingConfig.get_solo()
    tz_visitante = svc.zona_segura(data.get("zona_horaria"))

    validacion, motivo = svc.validar_slot(inicio)
    if not validacion:
        logger.info("Slot rechazado (%s) IP %s / correo %s.", motivo, ip, correo)
        return JsonResponse(
            {
                "success": False,
                "message": MENSAJES_SLOT.get(motivo, "El horario no está disponible."),
            },
            status=409,
        )

    telefono = f"{prefijo}{numero}"
    try:
        with transaction.atomic():
            lead = Lead.objects.filter(correo__iexact=correo).first()
            if lead is None:
                lead = Lead(
                    nombre=nombre,
                    correo=correo,
                    empresa=empresa or "No especificada",
                    mensaje=mensaje or None,
                    telefono=telefono,
                    ip_origen=ip,
                )
                # Silencia el flujo viejo (correo de "48 horas"): el booking
                # notifica por su cuenta con su propia task.
                lead.skip_email_signal = True
                lead.save()
            else:
                lead.telefono = telefono
                lead.ip_origen = ip
                if empresa:
                    lead.empresa = empresa
                if mensaje:
                    lead.mensaje = mensaje
                lead.save(update_fields=["telefono", "ip_origen", "actualizado_en"])

            # Estado + fecha/hora asignada por el cliente, SIN link de Meet
            # (meeting_link se mantiene vacío hasta que el equipo lo cargue
            # desde el CRM, dentro de las 24h prometidas).
            lead.meeting_at = inicio
            if lead.meeting_link:
                lead.meeting_link = ""  # nueva reunión futura: limpiar Meet viejo
                lead.save(
                    update_fields=["meeting_at", "meeting_link", "actualizado_en"]
                )
            else:
                lead.save(update_fields=["meeting_at", "actualizado_en"])
            transicionar_lead(
                lead,
                Lead.Estado.REUNION_CONFIRMADA,
                origen=LeadEstadoHistory.Origen.AUTOMATICO,
                nota=f"Agendado desde el booking público (tz {tz_visitante}).",
            )

            try:
                # SAVEPOINT anidado: en Postgres un IntegrityError deja la
                # transacción exterior abortada si no se aísla; con el
                # savepoint (mismo patrón de services/dedupe.py) queda limpia
                # y podemos responder 409 sin romper nada.
                with transaction.atomic():
                    appointment = Appointment.objects.create(
                        lead=lead,
                        inicio=inicio,
                        fin=inicio + datetime.timedelta(minutes=config.duracion_min),
                        duracion_min=config.duracion_min,
                        zona_horaria=tz_visitante,
                        consentimiento=True,
                        estado=Appointment.Estado.CONFIRMADA,
                    )
            except IntegrityError:
                # Race de dos peticiones por el mismo instante: la constraint
                # appointment_slot_confirmado_unico protege a nivel de BD.
                logger.info("Colisión de slot — IP %s / correo %s.", ip, correo)
                return JsonResponse(
                    {"success": False, "message": MENSAJES_SLOT["slot-ocupado"]},
                    status=409,
                )

            transaction.on_commit(
                lambda: async_task(
                    "apps.core.tasks.procesar_nuevo_agendamiento", appointment.pk
                )
            )
    except IntegrityError:
        logger.info("Colisión de slot (outer) — IP %s / correo %s.", ip, correo)
        return JsonResponse(
            {"success": False, "message": MENSAJES_SLOT["slot-ocupado"]},
            status=409,
        )

    logger.info(
        "Appointment %s creado para lead %s (correo %s, IP %s).",
        appointment.pk,
        lead.pk,
        correo,
        ip,
    )

    presentacion = svc.presentar(inicio, tz_visitante)
    return JsonResponse(
        {
            "success": True,
            "message": "¡Reunión agendada con éxito!",
            "appointment_id": appointment.pk,
            "lead_id": lead.pk,
            "fecha_hora_visitante": presentacion["visitante"],
            "fecha_hora_bogota": presentacion["bogota"],
            "zona_horaria": tz_visitante,
        },
        status=201,
    )

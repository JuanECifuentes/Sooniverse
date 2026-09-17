"""Verificación server-side de reCAPTCHA v3. Sin dependencias externas
(`requests` no está instalado en este proyecto; se usa urllib de la stdlib)."""

import json
import logging
import urllib.error
import urllib.parse
import urllib.request

from django.conf import settings

logger = logging.getLogger("django.apps.core.recaptcha")


def verify_recaptcha(
    token: str,
    remote_ip: str | None = None,
    expected_action: str | None = None,
) -> tuple[bool, str]:
    """Verifica un token de reCAPTCHA v3 contra la API de Google.

    `expected_action`: acción específica de este endpoint (p. ej.
    "contacto_lead" o "agenda_booking"). Si no se pasa, se usa
    settings.RECAPTCHA_ACTION (comportamiento legado del formulario).

    Devuelve (ok, reason).

    Degradación deliberada (fail-open):
    - Sin RECAPTCHA_SECRET_KEY configurada -> (True, "disabled"). El captcha
      queda desactivado hasta que se configuren las claves.
    - Si Google no responde (timeout/red) -> (True, "network-error"), con un
      warning en el log. El formulario ya tiene tres defensas independientes
      (honeypot, rate limit por IP, dedup de 24h en clean_correo); perder
      leads legítimos durante una caída de Google es peor que dejar pasar
      algunos bots.
    """
    secret = getattr(settings, "RECAPTCHA_SECRET_KEY", "")
    if not secret:
        return True, "disabled"
    if not token:
        return False, "missing-token"

    payload = {"secret": secret, "response": token}
    if remote_ip:
        payload["remoteip"] = remote_ip
    data = urllib.parse.urlencode(payload).encode()

    verify_url = getattr(
        settings,
        "RECAPTCHA_VERIFY_URL",
        "https://www.google.com/recaptcha/api/siteverify",
    )
    timeout = getattr(settings, "RECAPTCHA_TIMEOUT", 5)

    try:
        req = urllib.request.Request(verify_url, data=data)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result = json.loads(resp.read().decode())
    except (urllib.error.URLError, TimeoutError, ValueError, OSError) as exc:
        logger.warning("reCAPTCHA no verificable (fail-open): %s", exc)
        return True, "network-error"

    if not result.get("success"):
        return False, ",".join(result.get("error-codes", ["unknown"]))

    expected = expected_action or getattr(settings, "RECAPTCHA_ACTION", "contacto_lead")
    action = result.get("action")
    if action and action != expected:
        return False, f"action-mismatch:{action}"

    score = result.get("score", 0.0)
    min_score = getattr(settings, "RECAPTCHA_MIN_SCORE", 0.5)
    if score < min_score:
        return False, f"low-score:{score:.2f}"

    return True, f"ok:{score:.2f}"

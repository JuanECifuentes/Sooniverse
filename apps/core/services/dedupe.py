"""Deduplicación de notificaciones programadas basada en NotificationLog.

reclamar() intenta crear un NotificationLog con esa dedupe_key dentro de un
SAVEPOINT anidado (transaction.atomic()) y captura el IntegrityError de la
restricción unique — sin el savepoint, en Postgres un IntegrityError deja el
bloque atómico exterior envenenado (abortado) para el resto de la
transacción. Esto es lo que permite que dos workers de django-q2 compitiendo
por el mismo evento nunca envíen la misma notificación dos veces: solo uno
de los dos "reclama" la clave con éxito.
"""
import logging

from django.db import IntegrityError, transaction

from ..models import NotificationLog

logger = logging.getLogger("django.apps.core.dedupe")


def reclamar(kind: str, dedupe_key: str, *, lead=None, detalle: dict | None = None) -> bool:
    """Devuelve True solo la primera vez que se reclama esta dedupe_key."""
    try:
        with transaction.atomic():
            NotificationLog.objects.create(
                lead=lead, kind=kind, dedupe_key=dedupe_key, detalle=detalle or {}
            )
        return True
    except IntegrityError:
        logger.debug("dedupe_key ya reclamada, se omite: %s", dedupe_key)
        return False

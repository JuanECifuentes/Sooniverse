"""Signals for the core app.

The post_save signal on Lead centralizes the asynchronous email dispatch.
Internal Lead creation (admin panel / internal CRUD) can set the transient
attribute `skip_email_signal = True` on the instance before saving to mute
automated emails.
"""

import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from django_q.tasks import async_task

from .models import Lead

logger = logging.getLogger("django.apps.core.signals")


@receiver(post_save, sender=Lead)
def lead_post_save_dispatcher(sender, instance, created, **kwargs):
    """Enqueues notification emails only when a Lead is genuinely created
    from a public submission and not flagged for skipping."""
    if not created:
        return

    if getattr(instance, "skip_email_signal", False):
        logger.info(
            "Lead %s flagged with skip_email_signal; skipping notifications.",
            instance.pk,
        )
        return

    async_task("apps.core.tasks.procesar_nuevo_lead", instance.pk)

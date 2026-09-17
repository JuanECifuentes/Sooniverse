"""Crea/actualiza (idempotente) los Schedule de django-q2 que necesita el
CRM: el resumen diario y el barrido de reuniones inminentes.

Se elige un management command en vez de:
  - una migración de datos: es un disparo único, no repara un Schedule que
    alguien borró desde el admin ni corrige uno mal configurado.
  - AppConfig.ready(): corre en TODO proceso (incluidos `migrate` y
    `collectstatic` contra una base vacía, donde la tabla
    django_q_schedule aún no existe) — tocar la BD ahí es justo lo que
    la documentación de Django advierte no hacer.

Uso: python manage.py sync_schedules [--dry-run] [--force-next-run]

Orden de despliegue recomendado: migrate -> sync_schedules -> reiniciar
gunicorn -> reiniciar qcluster. Sin un `python manage.py qcluster` corriendo
como proceso supervisado, estos Schedule existen en la base de datos pero
nada los ejecuta.
"""
from datetime import timedelta
from datetime import timezone as dt_timezone
from zoneinfo import ZoneInfo

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from django_q.models import Schedule

DIGEST_SCHEDULE_NAME = "sooniverse-digest-diario"
SWEEPER_SCHEDULE_NAME = "sooniverse-reuniones-inminentes"


def _proximo_next_run_digest():
    tz = ZoneInfo("America/Bogota")
    hora_local = getattr(settings, "DIGEST_HORA_LOCAL", 8)
    ahora_bogota = timezone.localtime(timezone.now(), tz)
    objetivo = ahora_bogota.replace(hour=hora_local, minute=0, second=0, microsecond=0)
    if objetivo <= ahora_bogota:
        objetivo += timedelta(days=1)
    return objetivo.astimezone(dt_timezone.utc)


class Command(BaseCommand):
    help = "Crea/actualiza (idempotente) los Schedule de django-q2 del CRM."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Muestra qué se haría, sin escribir en la base de datos.",
        )
        parser.add_argument(
            "--force-next-run",
            action="store_true",
            help="Recalcula next_run aunque el Schedule ya exista (por defecto solo se fija al crear).",
        )

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        force_next_run = options["force_next_run"]

        definiciones = [
            {
                "name": DIGEST_SCHEDULE_NAME,
                "func": "apps.core.tasks.enviar_digest_diario",
                "schedule_type": Schedule.DAILY,
                "repeats": -1,
                "next_run_fn": _proximo_next_run_digest,
            },
            {
                "name": SWEEPER_SCHEDULE_NAME,
                "func": "apps.core.tasks.notificar_reuniones_inminentes",
                "schedule_type": Schedule.MINUTES,
                "minutes": 10,
                "repeats": -1,
                "next_run_fn": timezone.now,
            },
        ]

        for defn in definiciones:
            existente = Schedule.objects.filter(name=defn["name"]).first()
            defaults = {
                "func": defn["func"],
                "schedule_type": defn["schedule_type"],
                "repeats": defn["repeats"],
            }
            if "minutes" in defn:
                defaults["minutes"] = defn["minutes"]

            if existente is None or force_next_run:
                defaults["next_run"] = defn["next_run_fn"]()

            if dry_run:
                accion = "actualizaría" if existente else "crearía"
                self.stdout.write(f"[dry-run] se {accion} Schedule '{defn['name']}': {defaults}")
                continue

            _, created = Schedule.objects.update_or_create(name=defn["name"], defaults=defaults)
            accion = "creado" if created else "actualizado"
            self.stdout.write(self.style.SUCCESS(f"Schedule '{defn['name']}' {accion}."))

        if not dry_run:
            total = Schedule.objects.filter(
                name__in=[DIGEST_SCHEDULE_NAME, SWEEPER_SCHEDULE_NAME]
            ).count()
            self.stdout.write(f"Total de Schedule del CRM en la base de datos: {total}.")

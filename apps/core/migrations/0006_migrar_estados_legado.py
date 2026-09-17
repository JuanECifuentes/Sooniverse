"""Migra los Lead existentes de los 4 estados legado a los 10 del nuevo
pipeline, y deja un LeadEstadoHistory con origen=MIGRACION para cada fila
tocada (para que el operador pueda revisarlas manualmente, en particular las
que venían de "cerrado", que es ambiguo entre ganado y perdido).

Mapeo:
  nuevo       -> nuevo        (idéntico)
  contactado  -> contactado   (idéntico)
  en_proceso  -> contactado   (no afirma que ya se envió un diagnóstico;
                               "contactado" no genera recordatorios, así
                               que no dispara correos falsos)
  cerrado     -> servicio_realizado (ambiguo ganado/perdido; ambos destinos
                               candidatos son silenciosos; se deja nota
                               para revisión manual)

También rellena estado_actualizado_en = creado_en en todas las filas para
que el ancla del recordatorio de 7 días de "Nuevo" nunca sea NULL.
"""
from django.db import migrations

MAPEO = {
    "nuevo": "nuevo",
    "contactado": "contactado",
    "en_proceso": "contactado",
    "cerrado": "servicio_realizado",
}

NOTAS = {
    "en_proceso": "Migración 0006: estado legado 'en_proceso' mapeado a 'contactado'.",
    "cerrado": "Migración 0006: estado legado 'cerrado' mapeado a 'servicio_realizado' — revisar manualmente (puede haber sido un lead perdido, candidato a 'Descartado/Spam').",
}

MAPEO_REVERSO = {
    "nuevo": "nuevo",
    "contactado": "en_proceso",
    "reunion_confirmada": "en_proceso",
    "diagnostico_enviado": "en_proceso",
    "diagnostico_realizado": "en_proceso",
    "pre_implementacion": "en_proceso",
    "pendiente_implementacion": "en_proceso",
    "servicio_realizado": "cerrado",
    "descartado": "cerrado",
    "mantenimiento_programado": "en_proceso",
}


def migrar_hacia_adelante(apps, schema_editor):
    Lead = apps.get_model("core", "Lead")
    LeadEstadoHistory = apps.get_model("core", "LeadEstadoHistory")

    for legado, nuevo in MAPEO.items():
        if legado == nuevo:
            # Sin cambio de valor; estado_actualizado_en se backfillea para
            # TODAS las filas (incluidas estas) en el bucle final de abajo.
            continue

        leads = list(Lead.objects.filter(estado=legado))
        for lead in leads:
            LeadEstadoHistory.objects.create(
                lead=lead,
                estado_anterior=legado,
                estado_nuevo=nuevo,
                origen="MIGRACION",
                nota=NOTAS.get(legado, "Migración 0006: mapeo automático de estado legado."),
            )
        Lead.objects.filter(estado=legado).update(estado=nuevo)

    # Backfill: cualquier fila sin estado_actualizado_en toma su creado_en.
    for lead in Lead.objects.filter(estado_actualizado_en__isnull=True):
        lead.estado_actualizado_en = lead.creado_en
        lead.save(update_fields=["estado_actualizado_en"])


def migrar_hacia_atras(apps, schema_editor):
    Lead = apps.get_model("core", "Lead")
    LeadEstadoHistory = apps.get_model("core", "LeadEstadoHistory")

    for nuevo, legado in MAPEO_REVERSO.items():
        Lead.objects.filter(estado=nuevo).update(estado=legado)

    LeadEstadoHistory.objects.filter(origen="MIGRACION").delete()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0005_pipeline_estados"),
    ]

    operations = [
        migrations.RunPython(migrar_hacia_adelante, migrar_hacia_atras),
    ]

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_questionnaire_processinventory"),
    ]

    operations = [
        migrations.AddField(
            model_name="questionnaire",
            name="other_provider_name",
            field=models.CharField(
                blank=True,
                max_length=255,
                null=True,
                verbose_name="Nombre del proveedor alternativo",
            ),
        ),
        migrations.AddField(
            model_name="questionnaire",
            name="ai_tasks",
            field=models.JSONField(
                blank=True, default=list, verbose_name="Tareas y capacidades de IA"
            ),
        ),
        migrations.AlterField(
            model_name="questionnaire",
            name="traffic_pattern",
            field=models.CharField(
                blank=True,
                choices=[
                    ("ALL_REAL_TIME", "Todo en Tiempo Real"),
                    ("MOST_REAL_TIME", "Mayormente en Tiempo Real"),
                    ("MOST_BATCH", "Mayormente por Lotes"),
                    ("ALL_BATCH", "Todo por Lotes"),
                ],
                default="",
                max_length=32,
            ),
        ),
    ]

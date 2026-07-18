# Generated manually for QuestionnaireMetricFile upload support.

import django.db.models.deletion
import apps.core.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0003_questionnaire_v2_providers_tasks"),
    ]

    operations = [
        migrations.CreateModel(
            name="QuestionnaireMetricFile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        upload_to=apps.core.models.metric_file_upload_path,
                        verbose_name="Archivo de métricas",
                    ),
                ),
                (
                    "original_name",
                    models.CharField(
                        max_length=255,
                        verbose_name="Nombre original",
                    ),
                ),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)),
                (
                    "questionnaire",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="metric_files",
                        to="core.questionnaire",
                    ),
                ),
            ],
            options={
                "verbose_name": "Archivo de métricas",
                "verbose_name_plural": "Archivos de métricas",
                "ordering": ["uploaded_at"],
            },
        ),
    ]

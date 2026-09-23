from unittest.mock import patch

from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .forms import LeadForm, QuestionnaireMetricFileForm
from .models import Lead
from .tasks import procesar_nuevo_lead


class MetricFileFormTestCase(TestCase):
    def _file(self, name, size_mb):
        content = b"0" * (size_mb * 1024 * 1024)
        return SimpleUploadedFile(name, content, content_type="text/csv")

    def test_valid_csv_file(self):
        file = SimpleUploadedFile(
            "metrics.csv", b"date,requests\n2024-01-01,100\n", content_type="text/csv"
        )
        form = QuestionnaireMetricFileForm({}, {"metric_files": [file]})
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.cleaned_data["metric_files"]), 1)

    def test_invalid_extension_rejected(self):
        file = SimpleUploadedFile(
            "notes.txt", b"not allowed", content_type="text/plain"
        )
        form = QuestionnaireMetricFileForm({}, {"metric_files": [file]})
        self.assertFalse(form.is_valid())
        self.assertIn("metric_files", form.errors)

    def test_file_over_50mb_rejected(self):
        file = self._file("large.csv", 51)
        form = QuestionnaireMetricFileForm({}, {"metric_files": [file]})
        self.assertFalse(form.is_valid())
        self.assertIn("metric_files", form.errors)

    def test_more_than_10_files_rejected(self):
        files = [
            SimpleUploadedFile(f"m{i}.csv", b"a", content_type="text/csv")
            for i in range(11)
        ]
        form = QuestionnaireMetricFileForm({}, {"metric_files": files})
        self.assertFalse(form.is_valid())
        self.assertIn("metric_files", form.errors)


class LeadFormTestCase(TestCase):
    def test_valid_form(self):
        data = {
            "nombre": "Juan Cifuentes",
            "correo": "juan@example.com",
            "empresa": "Sooniverse Inc",
            "mensaje": "Quiero probar el diagnóstico.",
            "website_verification": "",
        }
        form = LeadForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        data = {
            "nombre": "Juan Cifuentes",
            "correo": "juan-invalid-email",
            "empresa": "Sooniverse Inc",
            "mensaje": "Quiero probar el diagnóstico.",
            "website_verification": "",
        }
        form = LeadForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("correo", form.errors)
        self.assertEqual(
            form.errors["correo"][0],
            "El correo electrónico ingresado no posee un formato válido para iniciar comunicación.",
        )

    def test_invalid_single_label_domain_email(self):
        data = {
            "nombre": "Juan Cifuentes",
            "correo": "juancifuentes124@com",
            "empresa": "Sooniverse Inc",
            "mensaje": "Quiero probar el diagnóstico.",
            "website_verification": "",
        }
        form = LeadForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("correo", form.errors)
        self.assertEqual(
            form.errors["correo"][0],
            "El correo electrónico ingresado no posee un formato válido para iniciar comunicación.",
        )

    def test_valid_multi_label_domain_email(self):
        data = {
            "nombre": "Juan Cifuentes",
            "correo": "juancifuentes124@sooniverse.com.co",
            "empresa": "Sooniverse Inc",
            "mensaje": "Quiero probar el diagnóstico.",
            "website_verification": "",
        }
        form = LeadForm(data=data)
        self.assertTrue(form.is_valid())

    def test_duplicate_email_within_24_hours(self):

        # Create an existing lead (skip email signal to isolate the test)
        lead = Lead(
            nombre="Duplicate Tester",
            correo="duplicate@example.com",
            empresa="Sooniverse",
        )
        lead.skip_email_signal = True
        lead.save()

        # Try to submit form with the same email
        data = {
            "nombre": "Duplicate Tester 2",
            "correo": "duplicate@example.com",
            "empresa": "Sooniverse 2",
            "mensaje": "Duplicate test message.",
            "website_verification": "",
        }
        form = LeadForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("correo", form.errors)
        self.assertEqual(
            form.errors["correo"][0],
            "Ya ha sido registrada una solicitud para este cliente.",
        )

    def test_duplicate_email_after_24_hours(self):
        from datetime import timedelta

        from django.utils import timezone

        # Create an old lead (skip email signal to isolate the test)
        lead = Lead(
            nombre="Old Tester",
            correo="old@example.com",
            empresa="Sooniverse",
        )
        lead.skip_email_signal = True
        lead.save()
        # Manually update creado_en since auto_now_add overrides creation input
        old_time = timezone.now() - timedelta(hours=25)
        Lead.objects.filter(pk=lead.pk).update(creado_en=old_time)

        # Try to submit form with the same email
        data = {
            "nombre": "Old Tester 2",
            "correo": "old@example.com",
            "empresa": "Sooniverse 2",
            "mensaje": "Duplicate test message.",
            "website_verification": "",
        }
        form = LeadForm(data=data)
        self.assertTrue(form.is_valid())

    def test_honeypot_bot_detected(self):
        data = {
            "nombre": "Juan Cifuentes",
            "correo": "juan@example.com",
            "empresa": "Sooniverse Inc",
            "mensaje": "Quiero probar el diagnóstico.",
            "website_verification": "I am a bot",
        }
        form = LeadForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("website_verification", form.errors)


class NotificationsTaskTestCase(TestCase):
    @patch("apps.core.services.notifications.EmailMultiAlternatives")
    def test_procesar_nuevo_lead_task(self, mock_email_class):
        # Create Lead (skip email signal — the task is invoked directly below)
        lead = Lead(
            nombre="Alice",
            correo="alice@wonderland.com",
            empresa="Wonderland",
            mensaje="Follow the white rabbit",
            ip_origen="127.0.0.1",
        )
        lead.skip_email_signal = True
        lead.save()

        # Execute the task
        procesar_nuevo_lead(lead.id)

        # Ensure EmailMultiAlternatives.send was called 2 times
        self.assertEqual(mock_email_class.return_value.send.call_count, 2)

        # Check call arguments
        # First call: Internal notification (recipient = admin@sooniverse.com)
        # Second call: Customer confirmation (recipient = alice@wonderland.com)
        call_args_list = mock_email_class.call_args_list

        first_call = call_args_list[0]
        from django.conf import settings

        self.assertEqual(
            first_call[1]["to"],
            [getattr(settings, "NOTIFICACION_INTERNA_EMAIL", "soporte@sooniverse.com")],
        )
        self.assertIn("[Nuevo Lead]", first_call[1]["subject"])

        second_call = call_args_list[1]
        self.assertEqual(second_call[1]["to"], ["alice@wonderland.com"])
        self.assertIn("reunión", second_call[1]["subject"])


class ManifestTestCase(TestCase):
    def test_manifest_success(self):
        url = reverse("core:manifest")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/json")
        data = response.json()
        self.assertEqual(data["name"], "Sooniverse")
        self.assertEqual(data["short_name"], "Sooniverse")
        self.assertTrue(len(data["icons"]) > 0)
        for icon in data["icons"]:
            self.assertTrue(icon["src"].startswith("/static/"))


class QuestionnaireFlowTestCase(TestCase):
    """Covers: UUID isolation, PENDING->COMPLETED flip, immutability, signal skip."""

    def _make_lead(self):
        lead = Lead(nombre="QA Lead", correo="qa@acme.io", empresa="Acme")
        lead.skip_email_signal = True
        lead.save()
        return lead

    def test_invalid_uuid_returns_404(self):
        # The <uuid:...> converter rejects non-UUIDs at routing -> 404.
        resp = self.client.get("/diagnostico/cuestionario/not-a-uuid/")
        self.assertEqual(resp.status_code, 404)

    @patch("apps.core.views.async_task")
    def test_pending_questionnaire_renders_form_and_completes_on_post(self, mock_async_task):
        from .models import Questionnaire

        lead = self._make_lead()
        q = Questionnaire.objects.create(lead=lead, status=Questionnaire.Status.PENDING)
        url = reverse(
            "core:public_questionnaire", kwargs={"questionnaire_id": str(q.id)}
        )

        get = self.client.get(url)
        self.assertEqual(get.status_code, 200)
        self.assertContains(get, "Bloque I")

        prefix = "processes"
        post_data = {
            "current_providers": ["OPENAI_CHATGPT", "ANTHROPIC_CLAUDE"],
            "monthly_spend": "12500.00",
            "traffic_pattern": Questionnaire.TrafficPattern.ALL_BATCH,
            f"{prefix}-TOTAL_FORMS": "1",
            f"{prefix}-INITIAL_FORMS": "0",
            f"{prefix}-MIN_NUM_FORMS": "0",
            f"{prefix}-MAX_NUM_FORMS": "1000",
            f"{prefix}-0-name": "Resumen de tickets",
            f"{prefix}-0-execution_type": "BATCH",
            f"{prefix}-0-input_tokens": "1200",
            f"{prefix}-0-output_tokens": "300",
            f"{prefix}-0-peak_concurrency": "",
            f"{prefix}-0-monthly_executions": "5000",
        }
        with self.captureOnCommitCallbacks(execute=True):
            post = self.client.post(url, post_data)
        self.assertEqual(post.status_code, 200)
        q.refresh_from_db()
        self.assertEqual(q.status, Questionnaire.Status.COMPLETED)
        self.assertIsNotNone(q.submitted_at)
        self.assertEqual(q.current_providers, ["OPENAI_CHATGPT", "ANTHROPIC_CLAUDE"])
        self.assertEqual(float(q.monthly_spend), 12500.00)
        self.assertEqual(q.processes.count(), 1)
        proc = q.processes.first()
        self.assertEqual(proc.name, "Resumen de tickets")
        self.assertEqual(proc.monthly_executions, 5000)
        self.assertIsNone(proc.peak_concurrency)

        # La finalización del cuestionario debe encolar la tarea de
        # notificación (via transaction.on_commit) con este questionnaire.id.
        mock_async_task.assert_called_once_with(
            "apps.core.tasks.notificar_diagnostico_completado", str(q.id)
        )

    def test_completed_questionnaire_is_immutable(self):
        from .models import Questionnaire

        lead = self._make_lead()
        q = Questionnaire.objects.create(
            lead=lead, status=Questionnaire.Status.COMPLETED
        )
        url = reverse(
            "core:public_questionnaire", kwargs={"questionnaire_id": str(q.id)}
        )
        post = self.client.post(
            url, {"current_providers": ["openai"], "monthly_spend": "9.99"}
        )
        self.assertEqual(post.status_code, 200)
        q.refresh_from_db()
        self.assertEqual(q.status, Questionnaire.Status.COMPLETED)
        self.assertIsNone(q.monthly_spend)
        self.assertEqual(q.current_providers, [])

    def test_public_questionnaire_with_file_upload(self):
        import os

        from .models import Questionnaire

        lead = self._make_lead()
        q = Questionnaire.objects.create(lead=lead, status=Questionnaire.Status.PENDING)
        url = reverse(
            "core:public_questionnaire", kwargs={"questionnaire_id": str(q.id)}
        )

        prefix = "processes"
        file = SimpleUploadedFile("metrics.csv", b"date,requests\n2024-01-01,100\n", content_type="text/csv")
        
        post_data = {
            "current_providers": ["OPENAI_CHATGPT"],
            "monthly_spend": "5000.00",
            "traffic_pattern": Questionnaire.TrafficPattern.ALL_BATCH,
            f"{prefix}-TOTAL_FORMS": "1",
            f"{prefix}-INITIAL_FORMS": "0",
            f"{prefix}-MIN_NUM_FORMS": "0",
            f"{prefix}-MAX_NUM_FORMS": "1000",
            f"{prefix}-0-name": "Test Process",
            f"{prefix}-0-execution_type": "BATCH",
            f"{prefix}-0-input_tokens": "100",
            f"{prefix}-0-output_tokens": "200",
            f"{prefix}-0-peak_concurrency": "",
            f"{prefix}-0-monthly_executions": "1000",
            "metric_files": [file],
        }
        
        resp = self.client.post(url, post_data)
        self.assertEqual(resp.status_code, 200)
        
        q.refresh_from_db()
        self.assertEqual(q.status, Questionnaire.Status.COMPLETED)
        self.assertEqual(q.metric_files.count(), 1)
        
        metric_file = q.metric_files.first()
        self.assertEqual(metric_file.original_name, "metrics.csv")
        self.assertTrue(metric_file.file.name.startswith(f"metrics_uploads/{q.id}/"))
        
        # Cleanup file after test
        if os.path.exists(metric_file.file.path):
            os.remove(metric_file.file.path)
            try:
                os.rmdir(os.path.dirname(metric_file.file.path))
            except OSError:
                pass

    def test_internal_lead_creation_skips_signal(self):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        user = User.objects.create_superuser("internal", "internal@sooniverse.com", "x")
        self.client.force_login(user)
        with patch("apps.core.signals.async_task") as mock_async:
            resp = self.client.post(
                reverse("core:internal_leads"),
                {
                    "nombre": "Manual",
                    "correo": "manual@acme.io",
                    "empresa": "Acme",
                    "estado": "nuevo",
                },
            )
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(Lead.objects.filter(correo="manual@acme.io").count(), 1)
        mock_async.assert_not_called()


class AuthenticationTests(TestCase):
    def test_login_required_redirects(self):
        # Accessing protected view redirects to login URL
        url = reverse("core:internal_leads")
        response = self.client.get(url)
        # It should redirect with the next parameter
        self.assertRedirects(response, f"/accounts/login/?next={url}")

    def test_login_page_renders(self):
        # Access login page directly
        url = reverse("core:login")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")
        self.assertContains(response, "Sooni")
        self.assertContains(response, "verse")
        self.assertContains(response, "ADVANCED TECH UNIVERSE")

    def test_login_success_redirects_to_internal_leads(self):
        from django.contrib.auth import get_user_model

        User = get_user_model()
        User.objects.create_user("testuser", "test@sooniverse.com", "password123")

        url = reverse("core:login")
        response = self.client.post(
            url, {"username": "testuser", "password": "password123"}
        )
        self.assertRedirects(response, reverse("core:internal_leads"))


class SecureDownloadViewTests(TestCase):
    def setUp(self):
        from django.contrib.auth import get_user_model

        from .models import Questionnaire, QuestionnaireMetricFile

        self.User = get_user_model()
        self.user = self.User.objects.create_user("testuser", "test@sooniverse.com", "password123")

        # Create lead, questionnaire, and metric file
        lead = Lead(nombre="Test", correo="t@t.com", empresa="Emp")
        lead.skip_email_signal = True  # avoid enqueuing a real notification task
        lead.save()
        self.q = Questionnaire.objects.create(lead=lead, status=Questionnaire.Status.COMPLETED)

        self.uploaded_file = SimpleUploadedFile("metrics.csv", b"date,requests\n2024-01-01,100\n", content_type="text/csv")
        self.metric_file = QuestionnaireMetricFile.objects.create(
            questionnaire=self.q,
            file=self.uploaded_file,
            original_name="metrics.csv"
        )

    def tearDown(self):
        import os
        if self.metric_file.file and os.path.exists(self.metric_file.file.path):
            os.remove(self.metric_file.file.path)
            try:
                os.rmdir(os.path.dirname(self.metric_file.file.path))
            except OSError:
                pass

    def test_anonymous_user_redirected_to_login(self):
        url = reverse("core:download_metric_file", kwargs={"file_id": self.metric_file.id})
        response = self.client.get(url)
        self.assertRedirects(response, f"/accounts/login/?next={url}")

    def test_authenticated_user_can_download(self):
        self.client.force_login(self.user)
        url = reverse("core:download_metric_file", kwargs={"file_id": self.metric_file.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Disposition"], 'attachment; filename="metrics.csv"')
        self.assertEqual(b"".join(response.streaming_content), b"date,requests\n2024-01-01,100\n")


# ──────────────────────────────────────────────────────────────
# Pipeline de 10 estados: transiciones, dedup y resumen diario
# ──────────────────────────────────────────────────────────────
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import transaction as db_transaction
from django.utils import timezone

from .models import (
    LeadEstadoHistory,
    MaintenanceWindow,
    NotificationLog,
    validar_limite_ventanas,
)
from .services.dedupe import reclamar
from .services.digest import construir_digest
from .services.pipeline import transicionar_lead
from .tasks import notificar_diagnostico_completado


def _lead_sin_email(**kwargs):
    lead = Lead(**kwargs)
    lead.skip_email_signal = True
    lead.save()
    return lead


class TransicionarLeadTestCase(TestCase):
    def test_transicion_escribe_historial_y_timestamp(self):
        lead = _lead_sin_email(nombre="A", correo="a@a.com", empresa="A", estado=Lead.Estado.NUEVO)
        antes = lead.estado_actualizado_en

        ok = transicionar_lead(lead, Lead.Estado.CONTACTADO, nota="test")
        self.assertTrue(ok)
        lead.refresh_from_db()
        self.assertEqual(lead.estado, Lead.Estado.CONTACTADO)
        self.assertNotEqual(lead.estado_actualizado_en, antes)

        hist = LeadEstadoHistory.objects.get(lead=lead)
        self.assertEqual(hist.estado_anterior, Lead.Estado.NUEVO)
        self.assertEqual(hist.estado_nuevo, Lead.Estado.CONTACTADO)
        self.assertEqual(hist.nota, "test")

    def test_transicion_no_op_devuelve_false(self):
        lead = _lead_sin_email(nombre="B", correo="b@b.com", empresa="B", estado=Lead.Estado.NUEVO)
        ok = transicionar_lead(lead, Lead.Estado.NUEVO)
        self.assertFalse(ok)
        self.assertEqual(LeadEstadoHistory.objects.filter(lead=lead).count(), 0)


class DedupeTestCase(TestCase):
    def test_reclamar_solo_la_primera_vez(self):
        primero = reclamar(NotificationLog.Kind.REUNION_INMINENTE, "clave-unica-1")
        segundo = reclamar(NotificationLog.Kind.REUNION_INMINENTE, "clave-unica-1")
        self.assertTrue(primero)
        self.assertFalse(segundo)
        self.assertEqual(NotificationLog.objects.filter(dedupe_key="clave-unica-1").count(), 1)

    def test_reclamar_no_envenena_transaccion_exterior(self):
        # reclamar() usa un savepoint anidado; un IntegrityError capturado
        # ahí no debe abortar un bloque atomic() exterior.
        with db_transaction.atomic():
            reclamar(NotificationLog.Kind.REUNION_INMINENTE, "clave-unica-2")
            reclamar(NotificationLog.Kind.REUNION_INMINENTE, "clave-unica-2")
            lead = Lead(nombre="C", correo="c@c.com", empresa="C")
            lead.skip_email_signal = True
            lead.save()
        self.assertEqual(Lead.objects.filter(correo="c@c.com").count(), 1)


class MaintenanceWindowLimitTestCase(TestCase):
    def test_septima_ventana_es_rechazada(self):
        lead = _lead_sin_email(nombre="D", correo="d@d.com", empresa="D")
        ahora = timezone.now()
        for i in range(MaintenanceWindow.MAX_POR_LEAD):
            MaintenanceWindow.objects.create(lead=lead, scheduled_for=ahora + timedelta(days=i + 1))
        self.assertEqual(lead.maintenance_windows.count(), 6)
        with self.assertRaises(ValidationError):
            validar_limite_ventanas(lead.pk)

    def test_excluir_pk_permite_editar_una_existente(self):
        lead = _lead_sin_email(nombre="E", correo="e@e.com", empresa="E")
        ahora = timezone.now()
        windows = [
            MaintenanceWindow.objects.create(lead=lead, scheduled_for=ahora + timedelta(days=i + 1))
            for i in range(MaintenanceWindow.MAX_POR_LEAD)
        ]
        # Editar una ventana existente (excluyéndola del conteo) no debe fallar.
        validar_limite_ventanas(lead.pk, exclude_pk=windows[0].pk)


class DigestBoundaryTestCase(TestCase):
    def test_lead_nuevo_dia_7_incluido_dia_8_excluido(self):
        # timezone.now() se fija con patch para evitar una carrera de
        # milisegundos entre el "ahora" de este test y el que calcula
        # construir_digest() -> _leads_nuevos_sin_atender() al reconstruir
        # su propio "limite" (now - 7 días) en un instante ligeramente
        # posterior.
        ahora_fija = timezone.now()
        hoy = timezone.localdate()

        lead_dia7 = _lead_sin_email(nombre="F7", correo="f7@f.com", empresa="F7")
        Lead.objects.filter(pk=lead_dia7.pk).update(
            estado_actualizado_en=ahora_fija - timedelta(days=7)
        )

        lead_dia8 = _lead_sin_email(nombre="F8", correo="f8@f.com", empresa="F8")
        Lead.objects.filter(pk=lead_dia8.pk).update(
            estado_actualizado_en=ahora_fija - timedelta(days=8)
        )

        with patch("apps.core.services.digest.timezone.now", return_value=ahora_fija):
            bloques = construir_digest(hoy)
        pks_incluidos = {item.lead.pk for item in bloques["leads_nuevos"]}
        self.assertIn(lead_dia7.pk, pks_incluidos)
        self.assertNotIn(lead_dia8.pk, pks_incluidos)

    def test_lead_descartado_nunca_aparece(self):
        hoy = timezone.localdate()
        lead = _lead_sin_email(
            nombre="G", correo="g@g.com", empresa="G", estado=Lead.Estado.DESCARTADO
        )
        Lead.objects.filter(pk=lead.pk).update(
            estado_actualizado_en=timezone.now() - timedelta(days=2)
        )
        bloques = construir_digest(hoy)
        pks = {item.lead.pk for item in bloques["leads_nuevos"]}
        self.assertNotIn(lead.pk, pks)

    def test_reprogramar_reunion_rearma_recordatorios(self):
        hoy = timezone.localdate()
        lead = _lead_sin_email(
            nombre="H", correo="h@h.com", empresa="H", estado=Lead.Estado.REUNION_CONFIRMADA
        )
        primera_fecha = timezone.now() + timedelta(days=3)
        lead.meeting_at = primera_fecha
        lead.save(update_fields=["meeting_at"])

        bloques = construir_digest(hoy)
        claves_antes = {item.dedupe_key for item in bloques["reuniones"]}
        self.assertTrue(any(str(lead.pk) in k for k in claves_antes))

        # Reclamar el recordatorio (simula que el digest ya se envió).
        for item in bloques["reuniones"]:
            reclamar(item.kind, item.dedupe_key, lead=item.lead)

        # Reprogramar la reunión a otra fecha (misma distancia en días) debe
        # generar una dedupe_key nueva porque incrusta meeting_at.isoformat().
        nueva_fecha = timezone.now() + timedelta(days=3, hours=5)
        lead.meeting_at = nueva_fecha
        lead.save(update_fields=["meeting_at"])

        bloques2 = construir_digest(hoy)
        claves_despues = {item.dedupe_key for item in bloques2["reuniones"]}
        self.assertTrue(claves_despues.isdisjoint(claves_antes))


class NotificarDiagnosticoCompletadoTestCase(TestCase):
    @patch("apps.core.services.notifications.EmailMultiAlternatives")
    def test_transiciona_lead_y_notifica_una_sola_vez(self, mock_email_class):
        from .models import Questionnaire

        lead = _lead_sin_email(
            nombre="I", correo="i@i.com", empresa="I", estado=Lead.Estado.DIAGNOSTICO_ENVIADO
        )
        q = Questionnaire.objects.create(lead=lead, status=Questionnaire.Status.COMPLETED)

        notificar_diagnostico_completado(str(q.id))
        lead.refresh_from_db()
        self.assertEqual(lead.estado, Lead.Estado.DIAGNOSTICO_REALIZADO)
        self.assertEqual(mock_email_class.return_value.send.call_count, 1)

        # Segunda llamada (p.ej. reintento de la tarea): no debe reenviar.
        notificar_diagnostico_completado(str(q.id))
        self.assertEqual(mock_email_class.return_value.send.call_count, 1)

    def test_lead_descartado_no_se_notifica(self):
        from .models import Questionnaire

        lead = _lead_sin_email(
            nombre="J", correo="j@j.com", empresa="J", estado=Lead.Estado.DESCARTADO
        )
        q = Questionnaire.objects.create(lead=lead, status=Questionnaire.Status.COMPLETED)
        notificar_diagnostico_completado(str(q.id))
        lead.refresh_from_db()
        self.assertEqual(lead.estado, Lead.Estado.DESCARTADO)
        self.assertEqual(NotificationLog.objects.filter(lead=lead).count(), 0)


class SyncSchedulesCommandTestCase(TestCase):
    def test_correr_dos_veces_deja_exactamente_dos_filas(self):
        from io import StringIO

        from django.core.management import call_command
        from django_q.models import Schedule

        call_command("sync_schedules", stdout=StringIO())
        call_command("sync_schedules", stdout=StringIO())

        nombres = {"sooniverse-digest-diario", "sooniverse-reuniones-inminentes"}
        self.assertEqual(Schedule.objects.filter(name__in=nombres).count(), 2)

    def test_dry_run_no_escribe_en_bd(self):
        from io import StringIO

        from django.core.management import call_command
        from django_q.models import Schedule

        call_command("sync_schedules", "--dry-run", stdout=StringIO())
        self.assertEqual(Schedule.objects.count(), 0)



# ──────────────────────────────────────────────
# Booking público (/agendar/)
# ──────────────────────────────────────────────

from datetime import datetime, time, timedelta
from datetime import timezone as dt_timezone
from zoneinfo import ZoneInfo

from django.conf import settings
from django.utils import timezone as dj_tz

from .models import Appointment, BookingConfig, DiaHorario
from .services import booking as booking_svc


def _siguiente_dia_habil(dias_adelante_minimo: int = 3):
    """Próximo día L-V (en Bogotá) al menos dias_adelante_minimo días en el
    futuro, para que sus slots pasen el filtro de antelación/ventana."""
    hoy_bogota = dj_tz.localtime().date()
    fecha = hoy_bogota + timedelta(days=dias_adelante_minimo)
    for _ in range(14):
        if fecha.weekday() < 5:
            return fecha
        fecha += timedelta(days=1)
    raise AssertionError("No se encontró día hábil cercano")


class BookingServiceTestCase(TestCase):
    """Generación de slots del motor de disponibilidad."""

    def test_slots_lunes_a_viernes(self):
        fecha = _siguiente_dia_habil(3)
        data = booking_svc.slots_para_fecha(fecha.isoformat(), "America/Bogota")
        self.assertEqual(data["zona_horaria"], "America/Bogota")
        self.assertTrue(data["slots"])
        primeros = [
            datetime.fromisoformat(s).astimezone(ZoneInfo(settings.TIME_ZONE))
            for s in data["slots"]
        ]
        # 9:00 (u hora actual legible) hasta 17:30 fin de jornada; slots cada 30 min.
        self.assertEqual(
            len(primeros), 18
        )  # 09:00..17:30 si el día completo está libre
        self.assertEqual((primeros[-1] - primeros[0]).total_seconds(), 17 * 1800)

    def test_fin_de_semana_sin_slots(self):
        hoy = dj_tz.localtime().date()
        fecha = hoy + timedelta(days=(6 - hoy.weekday()) % 7 or 7)  # próximo domingo
        data = booking_svc.slots_para_fecha(fecha.isoformat(), "America/Bogota")
        self.assertEqual(data["slots"], [])

    def test_zona_horaria_invalida_cae_en_colombia(self):
        data = booking_svc.slots_para_fecha(None, "Zona/Inventada")
        self.assertEqual(data["zona_horaria"], settings.TIME_ZONE)

    def test_slots_iguales_en_zonas_mismo_utc(self):
        """Bogotá y Lima comparten UTC: los slots listados son idénticos."""
        fecha = _siguiente_dia_habil(3)
        bogota = booking_svc.slots_para_fecha(fecha.isoformat(), "America/Bogota")
        lima = booking_svc.slots_para_fecha(fecha.isoformat(), "America/Lima")
        self.assertEqual(bogota["slots"], lima["slots"])
        self.assertEqual(lima["zona_horaria"], "America/Lima")


@override_settings(NOTIFICACION_INTERNA_EMAIL="admin@sooniverse.com")
class BookingAPIsTestCase(TestCase):
    def setUp(self):
        cache.clear()

    @staticmethod
    def _payload(inicio_iso, correo="cliente@empresa.com", consent=True):
        return {
            "inicio": inicio_iso,
            "zona_horaria": "America/Bogota",
            "nombre": "Jane Doe",
            "correo": correo,
            "telefono_prefijo": "+57",
            "telefono_numero": "3001234567",
            "empresa": "Stark Industries",
            "mensaje": "Quiero una plataforma privada de IA.",
            "consentimiento": consent,
            "website_verification": "",
            "g-recaptcha-response": "token-ok",
        }

    def _crear_slot(self):
        fecha = _siguiente_dia_habil(3)
        data = booking_svc.slots_para_fecha(fecha.isoformat(), "America/Bogota")
        self.assertTrue(data["slots"], "El fixture de slots debe producir slots")
        return data["slots"][0]

    @patch("apps.core.views_booking.async_task")
    @patch("apps.core.views_booking.verify_recaptcha", return_value=(True, "ok:1.00"))
    def test_reservar_exitoso(self, mock_recaptcha, mock_async_task):
        inicio = self._crear_slot()
        url = reverse("core:booking_reservar")
        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.post(
                url, data=self._payload(inicio), content_type="application/json"
            )
        self.assertEqual(response.status_code, 201, response.content)

        self.assertEqual(Lead.objects.count(), 1)
        lead = Lead.objects.first()
        self.assertEqual(lead.correo, "cliente@empresa.com")
        self.assertEqual(lead.telefono, "+573001234567")
        self.assertEqual(lead.estado, Lead.Estado.REUNION_CONFIRMADA)
        self.assertEqual(lead.meeting_at.isoformat(), inicio)
        self.assertEqual(lead.meeting_link, "")  # sin link de Meet

        self.assertEqual(Appointment.objects.count(), 1)
        appointment = Appointment.objects.first()
        self.assertEqual(appointment.estado, Appointment.Estado.CONFIRMADA)
        self.assertTrue(appointment.consentimiento)

        mock_async_task.assert_called_once_with(
            "apps.core.tasks.procesar_nuevo_agendamiento", appointment.pk
        )

    @patch(
        "apps.core.views_booking.verify_recaptcha",
        return_value=(False, "missing-token"),
    )
    def test_reservar_rechazada_sin_recaptcha(self, mock_recaptcha):
        inicio = self._crear_slot()
        url = reverse("core:booking_reservar")
        response = self.client.post(
            url, data=self._payload(inicio), content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Lead.objects.count(), 0)
        self.assertEqual(Appointment.objects.count(), 0)

    @patch("apps.core.views_booking.verify_recaptcha", return_value=(True, "ok:1.00"))
    def test_reservar_rechazada_sin_consentimiento(self, mock_recaptcha):
        inicio = self._crear_slot()
        url = reverse("core:booking_reservar")
        response = self.client.post(
            url,
            data=self._payload(inicio, consent=False),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("consentimiento", response.json()["message"])
        self.assertEqual(Appointment.objects.count(), 0)

    @patch("apps.core.views_booking.verify_recaptcha", return_value=(True, "ok:1.00"))
    def test_maximo_2_futuras_por_correo(self, mock_recaptcha):
        url = reverse("core:booking_reservar")
        inicios = []
        offset = 3
        fechas_vistas = set()
        while len(inicios) < 3 and offset < 30:
            data = booking_svc.slots_para_fecha(
                _siguiente_dia_habil(offset).isoformat(), "America/Bogota"
            )
            # Exige fechas DISTINTAS con slots libres (dos offsets pueden
            # caer en el mismo día hábil al saltar el fin de semana).
            if data["slots"] and data["fecha"] not in fechas_vistas:
                fechas_vistas.add(data["fecha"])
                inicios.append(data["slots"][0])
            offset += 1
        self.assertEqual(len(inicios), 3)

        for inicio in inicios[:2]:
            response = self.client.post(
                url,
                data=self._payload(inicio, correo="repetido@empresa.com"),
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 201, response.content)

        response = self.client.post(
            url,
            data=self._payload(inicios[2], correo="repetido@empresa.com"),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 429)
        self.assertEqual(Appointment.objects.count(), 2)

    @patch("apps.core.views_booking.async_task")
    @patch("apps.core.views_booking.verify_recaptcha", return_value=(True, "ok:1.00"))
    def test_doble_reserva_mismo_slot(self, mock_recaptcha, mock_async_task):
        inicio = self._crear_slot()
        url = reverse("core:booking_reservar")
        response1 = self.client.post(
            url,
            data=self._payload(inicio, correo="a@empresa.com"),
            content_type="application/json",
        )
        self.assertEqual(response1.status_code, 201)
        response2 = self.client.post(
            url,
            data=self._payload(inicio, correo="b@empresa.com"),
            content_type="application/json",
        )
        self.assertEqual(response2.status_code, 409)
        self.assertEqual(Appointment.objects.count(), 1)

    @patch("apps.core.views_booking.verify_recaptcha", return_value=(True, "ok:1.00"))
    def test_lead_existente_se_reutiliza(self, mock_recaptcha):
        Lead.objects.create(
            nombre="Lead Previo", correo="existente@empresa.com", empresa="Wayne Corp"
        )
        inicio = self._crear_slot()
        url = reverse("core:booking_reservar")
        response = self.client.post(
            url,
            data=self._payload(inicio, correo="existente@empresa.com"),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Lead.objects.count(), 1)
        lead = Lead.objects.first()
        self.assertEqual(lead.nombre, "Lead Previo")  # no se pisa el nombre
        self.assertEqual(lead.telefono, "+573001234567")
        self.assertEqual(lead.estado, Lead.Estado.REUNION_CONFIRMADA)

    @patch("apps.core.views_booking.verify_recaptcha", return_value=(True, "ok:1.00"))
    def test_honeypot_bloquea(self, mock_recaptcha):
        inicio = self._crear_slot()
        url = reverse("core:booking_reservar")
        payload = self._payload(inicio)
        payload["website_verification"] = "soy-un-bot"
        response = self.client.post(url, data=payload, content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Appointment.objects.count(), 0)

    @patch("apps.core.views_booking.verify_recaptcha", return_value=(True, "ok:1.00"))
    def test_disponibilidad_api(self, mock_recaptcha):
        url = reverse("core:booking_disponibilidad")
        response = self.client.get(
            f"{url}?tz=America/Bogota&g-recaptcha-response=token-ok"
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["success"])
        self.assertIn("fechas_disponibles", data)
        self.assertIn("slots", data)


class InternalAgendaTestCase(TestCase):
    """Módulo interno /interno/agenda/."""

    def setUp(self):
        from django.contrib.auth.models import User

        self.user = User.objects.create_user(username="op", password="x12345678")
        self.url = reverse("core:internal_agenda")

    def test_login_requerido(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("login", response.url)

    def _login(self):
        self.client.login(username="op", password="x12345678")

    def test_render_config(self):
        self._login()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Configuración del booking público")
        self.assertContains(response, "Lunes")
        self.assertContains(response, "Próximas citas")

    def _post_horarios(self, activo_desde=0, activo_hasta=4, inicio="08:00", fin="17:00"):
        self._login()
        data = {
            "csrfmiddlewaretoken": "x",
            "dias_apertura": 30,
            "duracion_min": 30,
            "anticipo_min": 60,
        }
        for dia in range(7):
            act = activo_desde <= dia <= activo_hasta
            data[f"dia_{dia}_activo"] = "on" if act else ""
            data[f"dia_{dia}_inicio"] = inicio
            data[f"dia_{dia}_fin"] = fin
        return self.client.post(self.url, data)

    @property
    def _activo(self):
        return None

    def test_guardar_configuracion(self):
        response = self._post_horarios()
        self.assertEqual(response.status_code, 302)
        sabado = DiaHorario.objects.get(dia=5)
        self.assertFalse(sabado.activo)
        lunes = DiaHorario.objects.get(dia=0)
        self.assertEqual(lunes.hora_inicio.strftime("%H:%M"), "08:00")

    def test_hora_inicio_mayor_a_fin_rechazada(self):
        response = self._post_horarios(0, 6, "18:00", "09:00")
        self.assertEqual(response.status_code, 200)  # re-render con error
        lunes = DiaHorario.objects.get(dia=0)
        self.assertEqual(lunes.hora_inicio.strftime("%H:%M"), "09:00")


@override_settings(NOTIFICACION_INTERNA_EMAIL="admin@sooniverse.com")
class ProcesoNuevoAgendamientoTestCase(TestCase):
    """Task de correos del booking, con dedupe por NotificationLog."""

    def _crear_cita(self):
        lead = Lead.objects.create(
            nombre="Jane Doe",
            correo="jane@company.com",
            empresa="Stark Industries",
            estado=Lead.Estado.REUNION_CONFIRMADA,
        )
        inicio = datetime(2026, 10, 9, 14, 0, tzinfo=dt_timezone.utc)
        return Appointment.objects.create(
            lead=lead,
            inicio=inicio,
            fin=inicio + timedelta(minutes=30),
            duracion_min=30,
            zona_horaria="America/Mexico_City",
            consentimiento=True,
        )

    @patch("apps.core.tasks.enviar_notificacion", return_value=True)
    def test_envia_confirmacion_y_aviso_interno(self, mock_envio):
        from .tasks import procesar_nuevo_agendamiento

        appointment = self._crear_cita()
        procesar_nuevo_agendamiento(appointment.pk)
        self.assertEqual(mock_envio.call_count, 2)
        destinatarios = [
            call.kwargs["destinatario"] for call in mock_envio.call_args_list
        ]
        self.assertIn("jane@company.com", destinatarios)
        self.assertIn("admin@sooniverse.com", destinatarios)

    @patch("apps.core.tasks.enviar_notificacion", return_value=True)
    def test_reprocesado_no_reenvia_por_dedupe(self, mock_envio):
        from .tasks import procesar_nuevo_agendamiento

        appointment = self._crear_cita()
        procesar_nuevo_agendamiento(appointment.pk)
        self.assertEqual(mock_envio.call_count, 2)
        # Reintento de la task (requeue del worker): los dedupe_keys ya
        # fueron reclamados, no debe enviarse nada más.
        procesar_nuevo_agendamiento(appointment.pk)
        self.assertEqual(mock_envio.call_count, 2)


class InmutabilidadCitasYSeguridadTestCase(TestCase):
    """Pruebas de inmutabilidad de citas existentes ante cambios de configuración
    interna y seguridad de agendamiento via API con reCAPTCHA."""

    def setUp(self):
        BookingConfig.objects.all().delete()
        DiaHorario.objects.all().delete()
        self.config = BookingConfig.objects.create(
            duracion_min=30,
            anticipo_min=120,
            dias_apertura=14,
        )
        for d in range(7):
            DiaHorario.objects.create(
                dia=d,
                activo=(d < 5),
                hora_inicio=time(9, 0),
                hora_fin=time(18, 0),
            )

    def test_cambio_configuracion_no_modifica_citas_existentes(self):
        """Un cambio interno en la duración de slots, antelación, días de apertura
        o días de horario laboral no altera las citas ya creadas ni las fechas
        comprometidas con los clientes."""
        lead = Lead.objects.create(
            nombre="Carlos Mendoza",
            correo="carlos@empresa.com",
            telefono="+573001234567",
            estado=Lead.Estado.REUNION_CONFIRMADA,
        )
        inicio_original = datetime(2026, 10, 15, 15, 0, tzinfo=dt_timezone.utc)
        fin_original = inicio_original + timedelta(minutes=30)
        lead.meeting_at = inicio_original
        lead.save()

        cita = Appointment.objects.create(
            lead=lead,
            inicio=inicio_original,
            fin=fin_original,
            duracion_min=30,
            zona_horaria="America/Bogota",
            consentimiento=True,
            estado=Appointment.Estado.CONFIRMADA,
        )

        # Se modifica drásticamente la configuración del sistema
        self.config.duracion_min = 60
        self.config.anticipo_min = 360
        self.config.dias_apertura = 3
        self.config.save()

        # Se modifica el horario del día y se desactiva
        dia_semana = inicio_original.astimezone(ZoneInfo("America/Bogota")).weekday()
        horario = DiaHorario.objects.get(dia=dia_semana)
        horario.activo = False
        horario.hora_inicio = time(14, 0)
        horario.hora_fin = time(16, 0)
        horario.save()

        # Verificar que la cita existente en BD permanece 100% intacta
        cita.refresh_from_db()
        lead.refresh_from_db()

        self.assertEqual(cita.inicio, inicio_original)
        self.assertEqual(cita.fin, fin_original)
        self.assertEqual(cita.duracion_min, 30)  # Mantiene su duración persistida
        self.assertEqual(cita.estado, Appointment.Estado.CONFIRMADA)
        self.assertEqual(lead.meeting_at, inicio_original)

        # La cita existente sigue ocupando su rango e impidiendo colisiones
        ocupado = Appointment.objects.filter(
            estado=Appointment.Estado.CONFIRMADA,
            inicio=inicio_original,
        ).exists()
        self.assertTrue(ocupado)

    @patch("apps.core.views_booking.verify_recaptcha")
    def test_api_reservar_sin_recaptcha_o_invalido_es_rechazada(self, mock_recaptcha):
        """La API de reservar debe rechazar sin excepción cualquier petición que
        no pase la verificación de reCAPTCHA."""
        import json

        url = reverse("core:booking_reservar")
        slot_inicio = datetime.now(dt_timezone.utc) + timedelta(days=2)
        slot_iso = slot_inicio.replace(microsecond=0).isoformat()

        # Caso 1: reCAPTCHA falla por token faltante o rechazado
        mock_recaptcha.return_value = (False, "missing-token")
        payload = {
            "inicio": slot_iso,
            "zona_horaria": "America/Bogota",
            "nombre": "Test Bot",
            "correo": "bot@spam.com",
            "telefono_prefijo": "+57",
            "telefono_numero": "3001234567",
            "consentimiento": True,
            "g-recaptcha-response": "",
        }
        res = self.client.post(
            url, data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(res.status_code, 403)
        self.assertEqual(Appointment.objects.count(), 0)

        # Caso 2: reCAPTCHA falla por acción incorrecta
        mock_recaptcha.return_value = (False, "action-mismatch:otra_accion")
        payload["g-recaptcha-response"] = "fake-token"
        res = self.client.post(
            url, data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(res.status_code, 403)
        self.assertEqual(Appointment.objects.count(), 0)

        # Caso 3: reCAPTCHA falla por score muy bajo (bot detectado)
        mock_recaptcha.return_value = (False, "low-score:0.10")
        res = self.client.post(
            url, data=json.dumps(payload), content_type="application/json"
        )
        self.assertEqual(res.status_code, 403)
        self.assertEqual(Appointment.objects.count(), 0)

    @patch("apps.core.views_booking.verify_recaptcha", return_value=(True, "ok:1.00"))
    def test_api_disponibilidad_retorna_mapa_en_lote(self, mock_recaptcha):
        """La API de disponibilidad debe devolver 'slots_por_fecha' y 'fechas_disponibles'
        para permitir carga en una sola petición."""
        url = reverse("core:booking_disponibilidad")
        res = self.client.get(
            url, {"tz": "America/Bogota", "g-recaptcha-response": "valid-token"}
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data["success"])
        self.assertIn("fechas_disponibles", data)
        self.assertIn("slots_por_fecha", data)
        self.assertIsInstance(data["fechas_disponibles"], list)
        self.assertIsInstance(data["slots_por_fecha"], dict)
        if data["fechas_disponibles"]:
            primera = data["fechas_disponibles"][0]
            self.assertIn(primera, data["slots_por_fecha"])


class InternalCotizacionesTestCase(TestCase):
    """Pruebas del módulo interno de cotizaciones (/interno/cotizaciones/)."""

    def setUp(self):
        from django.contrib.auth.models import User

        self.url = reverse("core:internal_cotizaciones")
        self.user = User.objects.create_user(
            username="analista", password="secretpassword123"
        )

    def test_acceso_anonimo_redirige_a_login(self):
        """Un usuario no autenticado debe ser redirigido a login."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)
        self.assertIn("next=/interno/cotizaciones/", response.url)

    def test_acceso_autenticado_renderiza_modulo_correctamente(self):
        """Un usuario autenticado puede acceder a la guía de cotización."""
        self.client.login(username="analista", password="secretpassword123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/internal/cotizaciones_dashboard.html")
        self.assertContains(response, "Guía de Cotización")
        self.assertContains(response, "Piso técnico")
        self.assertContains(response, "Mantenimiento programado")
        self.assertContains(response, "i_ingreso")



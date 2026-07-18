from django.test import TestCase, override_settings
from django.urls import reverse
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch

from .models import Lead
from .forms import LeadForm, QuestionnaireMetricFileForm
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
        from django.utils import timezone

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
        from django.utils import timezone
        from datetime import timedelta

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


@override_settings(
    RATE_LIMIT_LIMIT=3,
    RATE_LIMIT_WINDOW=60,
    NOTIFICACION_INTERNA_EMAIL="admin@sooniverse.com",
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
)
class ContactViewTestCase(TestCase):
    def setUp(self):
        cache.clear()

    @patch("apps.core.signals.async_task")
    def test_submit_lead_success(self, mock_async_task):
        url = reverse("core:contacto")
        data = {
            "nombre": "Jane Doe",
            "correo": "jane@company.com",
            "empresa": "Stark Industries",
            "mensaje": "Test message.",
            "website_verification": "",
        }
        response = self.client.post(url, data, HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])

        # Verify Lead saved in database
        self.assertEqual(Lead.objects.count(), 1)
        lead = Lead.objects.first()
        self.assertEqual(lead.nombre, "Jane Doe")
        self.assertEqual(lead.correo, "jane@company.com")
        self.assertEqual(lead.empresa, "Stark Industries")

        # Notifications are now dispatched via the post_save signal.
        mock_async_task.assert_called_once_with(
            "apps.core.tasks.procesar_nuevo_lead", lead.pk
        )

    @patch("apps.core.signals.async_task")
    def test_rate_limiting(self, mock_async_task):
        url = reverse("core:contacto")
        data = {
            "nombre": "Jane Doe",
            "correo": "jane@company.com",
            "empresa": "Stark Industries",
            "mensaje": "Test message.",
            "website_verification": "",
        }

        # Submit 3 times (limit is 3)
        for i in range(3):
            test_data = data.copy()
            test_data["correo"] = f"jane{i}@company.com"
            response = self.client.post(
                url, test_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
            )
            self.assertEqual(response.status_code, 200)

        # 4th submission must be blocked with 429
        test_data = data.copy()
        test_data["correo"] = "jane4@company.com"
        response = self.client.post(
            url, test_data, HTTP_X_REQUESTED_WITH="XMLHttpRequest"
        )
        self.assertEqual(response.status_code, 429)
        self.assertFalse(response.json()["success"])
        self.assertIn("Límite de solicitudes excedido", response.json()["message"])

        # Verify only 3 Leads saved in DB
        self.assertEqual(Lead.objects.count(), 3)


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
        self.assertIn("Diagnóstico Tecnológico", second_call[1]["subject"])


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

    def test_pending_questionnaire_renders_form_and_completes_on_post(self):
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
        from .models import Questionnaire, QuestionnaireMetricFile
        import os

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

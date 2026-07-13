"""URL routes for the core app."""

from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "core"

urlpatterns = [
    # Public landing / contact
    path("", views.landing, name="landing"),
    path("contacto/", views.contacto_lead, name="contacto"),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        name="robots_txt",
    ),
    path(
        "llms.txt",
        TemplateView.as_view(template_name="llms.txt", content_type="text/plain"),
        name="llms_txt",
    ),
    path(
        "sitemap.xml",
        TemplateView.as_view(
            template_name="sitemap.xml", content_type="application/xml"
        ),
        name="sitemap_xml",
    ),
    path("manifest.json", views.manifest, name="manifest"),
    # Public diagnostic questionnaire
    path(
        "diagnostico/cuestionario/<uuid:questionnaire_id>/",
        views.public_questionnaire,
        name="public_questionnaire",
    ),
    # Internal Lead CRUD + questionnaire management (staff only)
    path("interno/leads/", views.internal_leads_dashboard, name="internal_leads"),
    path(
        "interno/leads/<int:lead_pk>/cuestionarios/",
        views.questionnaire_modal_partial,
        name="questionnaire_modal",
    ),
    path(
        "interno/leads/<int:lead_pk>/cuestionarios/crear/",
        views.questionnaire_create,
        name="questionnaire_create",
    ),
    path(
        "interno/cuestionarios/<uuid:questionnaire_id>/respuestas/",
        views.questionnaire_answers_partial,
        name="questionnaire_answers",
    ),
]

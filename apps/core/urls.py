"""URL routes for the core app."""

from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import TemplateView

from . import views, views_booking

app_name = "core"

urlpatterns = [
    # Public landing / contact
    path("", views.landing, name="landing"),
    # Public booking (/agendar/)
    path("agendar/", views_booking.booking_publico, name="booking_publico"),
    path(
        "agendar/api/disponibilidad/",
        views_booking.booking_disponibilidad,
        name="booking_disponibilidad",
    ),
    path(
        "agendar/api/reservar/",
        views_booking.booking_reservar,
        name="booking_reservar",
    ),
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
    path(
        "interno/cuestionarios/archivos/<int:file_id>/descargar/",
        views.download_metric_file,
        name="download_metric_file",
    ),
    # Public diagnostic questionnaire
    path(
        "diagnostico/cuestionario/<uuid:questionnaire_id>/",
        views.public_questionnaire,
        name="public_questionnaire",
    ),
    # Internal Lead CRUD + questionnaire management (staff only)
    path("interno/leads/", views.internal_leads_dashboard, name="internal_leads"),
    # Internal module: Agenda (config del booking público + próximas citas)
    path("interno/agenda/", views.internal_agenda, name="internal_agenda"),
    # Internal module: Cotizaciones (Guía y calculadora de cotización)
    path(
        "interno/cotizaciones/",
        views.internal_cotizaciones,
        name="internal_cotizaciones",
    ),
    path(
        "interno/leads/estado/actualizar/",
        views.lead_update_status,
        name="lead_update_status",
    ),
    path(
        "interno/leads/<int:lead_pk>/detalle/",
        views.lead_detail_modal,
        name="lead_detail_modal",
    ),
    path(
        "interno/leads/<int:lead_pk>/reunion/",
        views.lead_meeting_update,
        name="lead_meeting_update",
    ),
    path(
        "interno/leads/<int:lead_pk>/mantenimientos/crear/",
        views.maintenance_window_create,
        name="maintenance_window_create",
    ),
    path(
        "interno/mantenimientos/<int:window_pk>/actualizar/",
        views.maintenance_window_update,
        name="maintenance_window_update",
    ),
    path(
        "interno/mantenimientos/<int:window_pk>/eliminar/",
        views.maintenance_window_delete,
        name="maintenance_window_delete",
    ),
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
    # Authentication
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
]

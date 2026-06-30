"""URL routes for the core app (Landing Page is fully public)."""

from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.landing, name="landing"),
]

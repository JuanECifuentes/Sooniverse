"""
Django settings for the Sooniverse project.
Single-file environment-aware configuration loaded via django-environ.

The active environment is selected with the DJANGO_ENV variable
(local | production). Defaults to "local" for development.
"""

import os
from pathlib import Path

import environ

# ──────────────────────────────────────────────
# Paths
# ──────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# ──────────────────────────────────────────────
# Environment selection
# ──────────────────────────────────────────────
DJANGO_ENV = os.getenv("DJANGO_ENV", "local").lower()

# ──────────────────────────────────────────────
# Environment variables
# ──────────────────────────────────────────────
env = environ.Env(
    DEBUG=(bool, False),
    LOCAL=(bool, False),
    TRM_CONTRACTUAL=(float, 4100.0),
)

env_file = BASE_DIR / ".env"
if env_file.exists():
    environ.Env.read_env(str(env_file))

# ──────────────────────────────────────────────
# Core
# ──────────────────────────────────────────────
SECRET_KEY = env("SECRET_KEY", default="insecure-dev-key-change-me")
# DEBUG and LOCAL are derived from DJANGO_ENV (not the .env file) so that
# promoting an environment to production is a one-line change.
DEBUG = DJANGO_ENV != "production"
LOCAL = DJANGO_ENV != "production"
ALLOWED_HOSTS = env.get_value("ALLOWED_HOSTS", default="localhost,127.0.0.1").split(",")

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ──────────────────────────────────────────────
# Applications
# ──────────────────────────────────────────────
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "django_q",
    "django_ses",
]

LOCAL_APPS = [
    "apps.core",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ──────────────────────────────────────────────
# Middleware
# ──────────────────────────────────────────────
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ──────────────────────────────────────────────
# Templates
# ──────────────────────────────────────────────
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ──────────────────────────────────────────────
# Database
# ──────────────────────────────────────────────
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "workforce_db"),
        "USER": os.getenv("DB_USER", "postgres"),
        "PASSWORD": os.getenv("DB_PASSWORD", "postgres"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

# ──────────────────────────────────────────────
# Password validation
# ──────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ──────────────────────────────────────────────
# Internationalization
# ──────────────────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ──────────────────────────────────────────────
# Static files
# ──────────────────────────────────────────────
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static", BASE_DIR / "img"]

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

# ──────────────────────────────────────────────
# Cache (Redis / LocMem)
# ──────────────────────────────────────────────
if LOCAL:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
            "LOCATION": "barbersync-local-mem",
        }
    }
else:
    REDIS_URL = env("REDIS_URL", default="redis://127.0.0.1:6379/1")
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
        }
    }

# ──────────────────────────────────────────────
# Django Q2
# ──────────────────────────────────────────────
Q_CLUSTER = {
    "name": env("Q_CLUSTER_NAME", default="sooniverse-q"),
    "workers": env.int("Q_CLUSTER_WORKERS", default=2),
    "timeout": env.int("Q_CLUSTER_TIMEOUT", default=90),
    "recycle": env.int("Q_CLUSTER_RECYCLER", default=300),
    "orm": "default",
}

# ──────────────────────────────────────────────
# Email
# ──────────────────────────────────────────────
if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = "django_ses.SESBackend"

AWS_SES_REGION_NAME = env("AWS_SES_REGION_NAME", default="us-east-1")
AWS_SES_REGION_ENDPOINT = env(
    "AWS_SES_REGION_ENDPOINT", default="email.us-east-1.amazonaws.com"
)
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="no-reply@sooniverse.com")

# ──────────────────────────────────────────────
# Security (production)
# ──────────────────────────────────────────────
if not DEBUG:
    print("DEBUG is False, setting security settings")
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"

# ──────────────────────────────────────────────
# Commercial settings
# ──────────────────────────────────────────────
TRM_CONTRACTUAL = env("TRM_CONTRACTUAL")

# ──────────────────────────────────────────────
# Active environment banner
# ──────────────────────────────────────────────
if DJANGO_ENV == "production":
    print(f"Running with PRODUCTION settings (DJANGO_ENV={DJANGO_ENV})")
else:
    print(f"Running with LOCAL settings (DJANGO_ENV={DJANGO_ENV})")

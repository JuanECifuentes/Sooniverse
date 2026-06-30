"""Production settings. Inherits from base.py and tightens security."""

from .base import *  # noqa: F401,F403

DEBUG = False
LOCAL = False

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

# In production we send mail via AWS SES.
EMAIL_BACKEND = "django_ses.SESBackend"

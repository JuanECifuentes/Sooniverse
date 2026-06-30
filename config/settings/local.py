"""Local development settings. Inherits from base.py."""

from .base import *  # noqa: F401,F403

DEBUG = True
LOCAL = True

# In local development the email backend is the console backend.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Print a friendly banner so devs know which settings module is active.
print("Running with LOCAL settings (config.settings.local)")

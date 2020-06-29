import os
from .settings import *  # noqa: F403

# This is NOT a complete production settings file. For more, see:
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

DEBUG = False

ALLOWED_HOSTS = ["*"]

STATIC_ROOT = os.path.join(BASE_DIR, "static")  # noqa: F405

STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

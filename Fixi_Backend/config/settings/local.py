import os

import environ
from pathlib import Path
from django.core.management.utils import get_random_secret_key

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = BASE_DIR / "Fixi_Backend"
env = environ.Env()
# GENERAL
# ------------------------------------------------------------------------------
DEBUG = env.bool("DJANGO_DEBUG", default=False)

SECRET_KEY = get_random_secret_key()
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=['*'])

# CACHES (Consider using a more persistent cache backend like Redis or Memcached in production)
# ------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": os.path.join(BASE_DIR, 'cache'),  # Define a dedicated cache directory
    }
}

# EMAIL
# ------------------------------------------------------------------------------
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = env('EMAIL_HOST', default='smtp.yourmailprovider.com')
EMAIL_USE_TLS = env.bool('EMAIL_USE_TLS', default=True)
EMAIL_PORT = env.int('EMAIL_PORT', default=587)
EMAIL_HOST_USER = env('EMAIL_HOST_USER', default='your-email@example.com')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# Celery
# ------------------------------------------------------------------------------
CELERY_TASK_EAGER_PROPAGATES = False  # Set to False in production to allow asynchronous task execution
CELERY_BROKER_URL = env("CELERY_BROKER_URL", default="redis://localhost:6379/0")  # Adjust as needed

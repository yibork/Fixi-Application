from .base import *  # noqa
from .base import env
from django.core.management.utils import get_random_secret_key

DEBUG = True
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default=get_random_secret_key(),
)
ALLOWED_HOSTS = ['*']

# Celery Configuration Options
# ------------------------------------------------------------------------------

# Celery uses a broker to pass messages between your application and Celery worker processes.

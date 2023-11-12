from .base import *  # noqa
from .base import env

DEBUG = True
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default='z8q1(&_jk0zu#wc!$7#mkf6a$^3@69o87bf$b0-q#u3m%a30yq',
)
ALLOWED_HOSTS = ['*']

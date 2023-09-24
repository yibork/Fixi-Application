"""
Django settings for Fixi_Backend project.

Generated by 'django-admin startproject' using Django 2.2.11.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import environ
from pathlib import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
APPS_DIR = BASE_DIR / "Fixi_Backend"
env = environ.Env()


READ_DOT_ENV_FILE = env.bool("DJANGO_READ_DOT_ENV_FILE", default=False)
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    print("reading .env file")
    env.read_env(str(BASE_DIR / ".env"))
else:
    print("reading .env.dev file")
    env.read_env(str(BASE_DIR / ".env.dev"))

# GENERAL

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z8q1(&_jk0zu#wc!$7#mkf6a$^3@69o87bf$b0-q#u3m%a30yq'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
USE_X_FORWARDED_HOST = True

# In settings.py
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Application definition

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

]
THIRD_PARTY_APPS = [
    'allauth',
    'allauth.account',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'pictures',
    'treebeard',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'taggit',
    'dj_rest_auth.registration',
    'colorfield',
    'django_filters',
    "channels",
]
LOCAL_APPS =[
"Fixi_Backend.Catalogue",
"Fixi_Backend.users",
"Fixi_Backend.promotions",
"Fixi_Backend.basket",
"Fixi_Backend.orders",
"Fixi_Backend.reviews",
"Fixi_Backend.chat",
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = "config.urls"
DJANGO_ADMIN_URL = "django-admin/"

CORS_ALLOW_ALL_ORIGINS = True
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        # "rest_framework.authentication.TokenAuthentication",
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    # 'DEFAULT_PAGINATION_CLASS': 'yanvision_shop.utils.CustomPageNumberPagination',
}
REST_AUTH = {
    'USE_JWT': True,
    "JWT_AUTH_HTTPONLY": False,
    'OLD_PASSWORD_FIELD_ENABLED': True,
    'USER_DETAILS_SERIALIZER': 'Fixi_Backend.users.serializers.UserSerializer',
    #
}
AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'Fixi_Backend.users.serializers.UserSerializer',
}
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
AUTH_USER_MODEL = "users.User"

# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "users:redirect"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = "account_login"
ASGI_APPLICATION = "ChatAPI.asgi.application"

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Fixi_Backend.wsgi.application'


# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES ={
    "default": {
        'ENGINE': "django.db.backends.postgresql",
        'NAME': "railway",
        'USER': "postgres",
        'PASSWORD': "YFkFwOGBOaY8Z18vCOO0",
        'HOST': "containers-us-west-171.railway.app",
        'PORT': "6050",
    }
}
DATABASES["default"]["ATOMIC_REQUESTS"] = True

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True






# ------------------------------------------------------------------------------
ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = "username"
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_REQUIRED = True
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_EMAIL_VERIFICATION = "optional"
# https://django-allauth.readthedocs.io/en/latest/configuration.html

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'APP': {
            'client_id': '753733306504277',
            'secret': '7c82bfb42100067233f0ecbbc41fff5b',
            'key': '',
        }
    }
}

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '1010540222711-e79iioq7ti2jr1665674f9ip7dm9d9vd.apps.googleusercontent.com',
            'secret': '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',
            'key': '',
        }
    }
}
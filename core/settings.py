"""
Django settings for socialsite project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path
from .all_settings import settings
from env.load_env import load_environment_variables

# LOADING ENVS
load_environment_variables()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-%#7f3c!k-8+6-e@ij5%2l@9yl-*4=&(1zf%6w1t7y(&&ld$26%"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.getenv("DEBUG"))

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = settings["installed_apps"]()

MIDDLEWARE = settings["middleware"]()

ROOT_URLCONF = "core.urls"

TEMPLATES = settings["templates"]()

WSGI_APPLICATION = "core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = settings["databases"]()

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = settings["auth_password_validators"]()


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

"""
THIRD PARTY SETTINGS
"""
REST_FRAMEWORK = settings["rest_framework"]()
SIMPLE_JWT = settings["simple_jwt"]()
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

AUTH_USER_MODEL = "authsys.User"

"""
Django settings for common project.

Generated by 'django-admin startproject' using Django 3.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

import os
import json

# Build paths inside the project like this: BASE_DIR / 'subdir'.
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
BASE_DIR = os.path.join(ROOT_DIR, 'src')
RESOURCES_DIR = os.path.join(ROOT_DIR, 'resources')
PRIVATE_DIR = os.path.join(RESOURCES_DIR, 'private')
DATABASE_SETTING_DIR = os.path.join(PRIVATE_DIR, 'database')
SETTING_PATH = os.path.join(PRIVATE_DIR, 'settings.json')
SETTING_FILE = json.loads(open(SETTING_PATH).read())

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SETTING_FILE['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Session
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'
SESSION_COOKIE_AGE = 60 * 60 * 6

# Log
LOGGING = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s [%(filename)s:%(funcName)s:\
                %(lineno)s] %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        },
        'sql': {
            'format': '[%(asctime)s] %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'handlers': {
        'production-console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        }
    },
    'loggers': {
        'django.template': {
            'propagate': False
        },
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
        'connect': {
            'handlers': ['production-console'],
            'level': 'DEBUG'
        }
    }
}


REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'doc.schemas.CustomSchema',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'common.pagination.CustomLimitOffSetPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': ['user.auth.authentications.JSONWebTokenAuthentication'],
    'EXCEPTION_HANDLER': 'common.middlewares.custom_exception_handler'
}


SPECTACULAR_SETTINGS = {
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'filter': '',
    },
    'SERVE_PERMISSIONS': ['common.permissions.IsAdminUser'],
    'SERVE_INCLUDE_SCHEMA': False,
    'TITLE': 'Connect API',
    'DESCRIPTION': '**Swagger Link** : <a href="/docs/swagger" title="Hobbit lifestyles">/docs/swagger</a> <br/> **ReDoc Link** : <a href="/docs/redoc" title="Hobbit lifestyles">/docs/redoc</a>',
    'VERSION': '1.0.0',
}


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'rest_framework',
    'corsheaders',
    'drf_spectacular',
    'common',
    'user',
    'feed',
    'image',
    'doc'
]

# MiddleWare

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'common.urls'


# Templates
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

# Upload File
FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440
FILE_UPLOAD_MAX_SIZE = 5242880

# Django Url Settings
APPEND_SLASH = False

# Media
MEDIA_ROOT = os.path.join(ROOT_DIR, '.media')
MEDIA_URL = '/media/'

# Static
STATIC_ROOT = os.path.join(ROOT_DIR, '.static')
STATIC_URL = '/static/'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(PRIVATE_DIR, "database/mysql_debug.cnf")
        }
    }
}

# Email

EMAIL_HOST = SETTING_FILE['EMAIL']['HOST']
EMAIL_PORT = SETTING_FILE['EMAIL']['PORT']
EMAIL_HOST_USER = SETTING_FILE['EMAIL']['HOST_USER']
EMAIL_HOST_PASSWORD = SETTING_FILE['EMAIL']['HOST_PASSWORD']
EMAIL_USE_TLS = SETTING_FILE['EMAIL']['USER_TLS']
DEFAULT_FROM_EMAIL = SETTING_FILE['EMAIL']['HOST_USER']

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
AUTH_USER_MODEL = 'user.User'


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'ko'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Site

SITE_ID = 1


# Error

NON_FIELD_ERRORS_KEY = 'errors'

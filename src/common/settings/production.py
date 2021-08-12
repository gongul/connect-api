from .base import *
from .base import DATABASE_SETTING_DIR, os

ALLOWED_HOSTS = ["*"]

DEBUG = False

WSGI_APPLICATION = 'common.wsgi.production.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(DATABASE_SETTING_DIR, "mysql_production.cnf")
        }
    }
}

SESSION_COOKIE_SECURE = True

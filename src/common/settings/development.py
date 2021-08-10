from .base import DATABASE_SETTING_DIR, os

ALLOWED_HOSTS = ["*"]

DEBUG = True

INTERNAL_IPS = ('127.0.0.1',)

WSGI_APPLICATION = 'common.wsgi.development.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(DATABASE_SETTING_DIR, "mysql_development.cnf"),
        }
    }
}

SESSION_COOKIE_SECURE = False

# CORS
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

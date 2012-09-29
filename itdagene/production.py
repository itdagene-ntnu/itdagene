from itdagene.settings import *
import sys
POSTGRESQL = True

with open('/django-sites/mail-pw/noreply', 'rb') as f:
    mail_password = f.readline()
mail_password = mail_password.replace("\n","").strip()

with open('/django-sites/db-pw/prod', 'rb') as f:
    db_password = f.readline()
db_password = db_password.replace("\n","").strip()

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django-prod',
        'USER': 'django-prod',
        'PASSWORD': db_password,
        'HOST': '127.0.0.1',
        'PORT': ''
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'noreply@itdagene.no'
EMAIL_HOST_PASSWORD = mail_password
EMAIL_USE_TLS = True
#SESSION_COOKIE_SECURE = True

sys.stdout = sys.stderr



CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',
    }
}


LANGUAGE_CODE = 'en'
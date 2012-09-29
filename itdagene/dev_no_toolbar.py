from itdagene.settings import *
DEBUG=True
TOOLBAR=False
POSTGRESQL = True
TEMPLATE_DEBUG=DEBUG

try:
    with open('/django-sites/db-pw/dev', 'rb') as f:
        db_password = f.readline()
    db_password = db_password.replace("\n","").strip()
except:
    db_password = ""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django-dev',
        'USER': 'django-dev',
        'PASSWORD': db_password,
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
MAIL_SENDMAIL_EXECUTABLE  = "/usr/sbin/sendmail-demo"

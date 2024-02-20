from itdagene.settings.base import INSTALLED_APPS  # ? Unused import

DATABASES = {
    "TEST": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "itdagene",
        "USER": "itdagene",
        "PASSWORD": "itdagene",
        "HOST": "127.0.0.1",
        "PORT": "",
    },
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "itdagene",
        "USER": "itdagene",
        "PASSWORD": "itdagene",
        "HOST": "127.0.0.1",
        "PORT": "",
    },
}
SECRET_KEY = "testing"
DEFAULT_LANGUAGE = "nb"

CELERY_TASK_ALWAYS_EAGER = True
CELERY_BROKER_URL = "redis://"
CELERY_RESULT_BACKEND = "redis://"

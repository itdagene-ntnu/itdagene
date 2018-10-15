from .base import GRAPHENE
from .debug_toolbar import *

DEBUG = True
THUMBNAIL_DEBUG = False
HOST_URL = "http://localhost:8000"
ALLOWED_HOSTS = ['*']
TOOLBAR = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'itdagene',
        'USER': 'itdagene',
        'PASSWORD': 'itdagene',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}
GRAPHENE['MIDDLEWARE'] += [
    'graphene_django.debug.DjangoDebugMiddleware',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}

CORS_ORIGIN_WHITELIST = ('localhost:3000', "next.itdagene.no", "itdagene.no")
CELERY_TASK_ALWAYS_EAGER = True
CELERY_BROKER_URL = 'redis://'
CELERY_RESULT_BACKEND = 'redis://'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

import os
import sys

from django.contrib.messages import ERROR, INFO, SUCCESS, WARNING
from django.utils.translation import gettext_lazy as _


SITE = {
    "project_name": "itDAGENE 2018",
    "name": "itDAGENE",
    "email": "web@itdagene.no",
    "contact_email": "styret@itdagene.no",
    "domain": "itdagene.no",
    "mail_base": "https://itdagene.no",
    "address": "Sem Sælands vei 7-9",
    "town": "Trondheim",
    "zip_code": "7491",
    "organization_number": "912 601 625",
    "analytics": "UA-111908666-1",
    "drift_mail_prefix": "web",
    "description": "itDAGENE er en arbeidslivsmesse hvor studenter blir kjent med fremtidige "
    "arbeidsgivere. Messen arrangeres av studenter for studenter, overskuddet går "
    "til studentenes ekskursjon i tredjeklasse. itDAGENE arrangeres en gang i året "
    "av data- og kommunikasjonsteknologi ved NTNU i Trondheim.",
    "twitter_username": "@itDAGENE",
    "twitter_url": "https://twitter.com/itDAGENE",
    "instagram_tag": "ITDAGENE",
}

PATH = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PATH, "itdagene"))

ALLOWED_HOSTS = []

SHELL_PLUS = "ipython"

ADMINS = (("itDAGENE Web", f"{SITE['drift_mail_prefix']}@itdagene.no"),)
MANAGERS = ADMINS

THUMBNAIL_UPSCALE = False

USE_I18N = True
USE_L10N = True
USE_TZ = True

"""
DATE_FORMAT = 'd.m.Y'
TIME_FORMAT = 'H:i'
DATETIME_FORMAT = DATE_FORMAT + ' ' + TIME_FORMAT
"""

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"

LANGUAGE_CODE = "nb"
DEFAULT_LANGUAGE = "nb"
LANGUAGES = (("nb", "Norsk"), ("en", "English"))

LOCALE_PATHS = (os.path.join(PATH, "locale"),)

PROFILE_TYPES = (
    ("b", _("Board member")),
    ("c", _("Company profile")),
    ("w", _("Workers")),
    ("u", _("Unknown")),
)

TIME_ZONE = "Europe/Oslo"

MEDIA_ROOT = os.path.join(PATH, "files", "uploads")
MEDIA_URL = "/uploads/"

STATIC_ROOT = os.path.join(PATH, "files", "static")
STATIC_URL = "/static/"

STATICFILES_DIRS = (os.path.join(PATH, "assets"),)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)
INTERNAL_IPS = ("127.0.0.1",)

MIDDLEWARE = [
    "raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "itdagene.core.middleware.ForceDefaultLanguageMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "itdagene.core.notifications.middleware.NotificationsMiddleware",
    "itdagene.core.middleware.CurrentUserMiddleware",
    "social_django.middleware.SocialAuthExceptionMiddleware",
]

ROOT_URLCONF = "itdagene.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.contrib.admin",
    "raven.contrib.django.raven_compat",
    "django_extensions",
    "widget_tweaks",
    "sorl.thumbnail",
    "crispy_forms",
    "social_django",
    "itdagene.core",
    "itdagene.core.notifications",
    "itdagene.core.log",
    "itdagene.graphql",
    "itdagene.app.frontpage",
    "itdagene.app.pages",
    "itdagene.app.faq",
    "itdagene.app.news",
    "itdagene.app.mail",
    "itdagene.app.users",
    "itdagene.app.itdageneadmin",
    "itdagene.app.company",
    "itdagene.app.career",
    "itdagene.app.comments",
    "itdagene.app.events",
    "itdagene.app.feedback",
    "itdagene.app.meetings",
    "itdagene.app.todo",
    "itdagene.app.workschedule",
    "itdagene.app.experiences",
    "itdagene.app.stands",
    "itdagene.app.gallery",
    "graphene_django",
    "corsheaders",
]

APP_KEY = ""
APP_SECRET = ""

OAUTH_TOKEN = ""
OAUTH_TOKEN_SECRET = ""

TOOLBAR = False

GOOGLE_AUTH = False

CRISPY_TEMPLATE_PACK = "bootstrap4"

AUTH_USER_MODEL = "core.User"

EMAIL_SUBJECT_PREFIX = f"[{SITE['name']}] "
SERVER_EMAIL = f"{SITE['name']} <{SITE['email']}>"
DEFAULT_FROM_EMAIL = SERVER_EMAIL

MESSAGE_TAGS = {
    SUCCESS: "success",
    INFO: "info",
    WARNING: "warning",
    ERROR: "danger",
}

CORS_ORIGIN_WHITELIST = ("https://itdagene.no",)
GRAPHENE = {
    "MIDDLEWARE": [
        "itdagene.graphql.middleware.LoaderMiddleware",
        "itdagene.graphql.middleware.ResolveLimitMiddleware",
    ],
    "SCHEMA": "itdagene.graphql.schema.schema",
}

GRAPHENE_RESOLVER_LIMIT = 3000

# CELERY
CELERY_TASK_SERIALIZER = "pickle"
CELERY_RESULT_SERIALIZER = "pickle"
CELERY_ACCEPT_CONTENT = ["pickle"]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(PATH, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
                "itdagene.core.context_processors.site_processor",
                "itdagene.core.context_processors.utils_processor",
                "itdagene.app.pages.context_processors.menu_pages",
            ]
        },
    }
]

# Metabase config
METABASE_SITE_URL = ""
METABASE_SECRET_KEY = ""

TESTING = "test" in sys.argv  # Check if manage.py test has been run


def skip_if_testing(*args, **kwargs) -> bool:
    return not TESTING


LOGGING = {
    "version": 1,
    "disable_existing_loggers": True,
    "root": {"level": "DEBUG", "handlers": ["sentry", "console", "syslog"]},
    "filters": {
        "skip_if_testing": {
            "()": "django.utils.log.CallbackFilter",
            "callback": skip_if_testing,
        }
    },
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        }
    },
    "handlers": {
        "sentry": {
            "level": "WARNING",
            "filters": ["skip_if_testing"],
            "class": "raven.contrib.django.raven_compat.handlers.SentryHandler",
        },
        "console": {
            "level": "DEBUG",
            "filters": ["skip_if_testing"],
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "syslog": {
            "level": "INFO",
            "class": "logging.handlers.SysLogHandler",
            "facility": "local7",
            "formatter": "verbose",
        },
        "null": {"level": "DEBUG", "class": "logging.NullHandler"},
    },
    "loggers": {
        "raven": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
        "sentry.errors": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
        "django.security.DisallowedHost": {
            "handlers": ["null"],
            "propagate": False,
        },
    },
}

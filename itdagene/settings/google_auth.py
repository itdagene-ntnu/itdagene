import os
import sys

from itdagene.settings.base import AUTH_USER_MODEL
# from itdagene.settings.debug_toolbar import MIDDLEWARE

# Usage:
# You must provide these in your config:
# from itdagene.settings.google_auth import *
# SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ""
# SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ""

PATH = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, os.path.join(PATH, "itdagene"))

AUTHENTICATION_BACKENDS = (
    "social_core.backends.google.GoogleOAuth2",
    "django.contrib.auth.backends.ModelBackend",
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(PATH, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "itdagene.core.context_processors.site_processor",
                "itdagene.core.context_processors.utils_processor",
                "itdagene.app.pages.context_processors.menu_pages",
            ]
        },
    }
]

SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "itdagene.core.models.auth_allowed",
    # "social_core.pipeline.social_auth.auth_allowed",
    "social_core.pipeline.social_auth.load_extra_data",
    "itdagene.core.models.get_user",
    "social.pipeline.social_auth.associate_user",
)

SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

SOCIAL_AUTH_GOOGLE_OAUTH2_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]
SOCIAL_AUTH_USER_MODEL = AUTH_USER_MODEL
SOCIAL_AUTH_LOGIN_ERROR_URL = "/login/?error=true"

SOCIAL_AUTH_GOOGLE_OAUTH2_WHITELISTED_DOMAINS = ["itdagene.no"]

GOOGLE_AUTH = True

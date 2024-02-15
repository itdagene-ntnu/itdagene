from typing import Optional

from django.http import HttpRequest
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from itdagene.core.auth import set_current_user_function
from itdagene.core.models import Preference


class ForceDefaultLanguageMiddleware(MiddlewareMixin):
    """Ignore Accept-Language HTTP headers.

    This will force the I18N machinery to always choose
    settings.LANGUAGE_CODE as the default initial language, unless
    another one is set via sessions or cookies.

    Should be installed `before` any middleware that checks
    request.META['HTTP_ACCEPT_LANGUAGE'], namely
    django.middleware.locale.LocaleMiddleware.
    """

    def process_request(self, request: HttpRequest) -> None:
        http_accept_language = "HTTP_ACCEPT_LANGUAGE"
        if http_accept_language in request.META:
            del request.META[http_accept_language]


class UnderDevelopmentMiddleware(MiddlewareMixin):
    def process_request(self, request: HttpRequest) -> Optional[HttpResponseRedirect]:
        if request.path == reverse("itdagene.under_development"):
            return
        if "login" in request.path:
            return
        if not Preference.current_preference().development_mode:
            return
        if request.user.is_authenticated and request.user.is_staff:
            return
        return HttpResponseRedirect(reverse("itdagene.under_development"))


class CurrentUserMiddleware(MiddlewareMixin):
    def process_request(self, request: HttpRequest) -> None:
        user = getattr(request, "user", None)
        set_current_user_function(lambda: user)

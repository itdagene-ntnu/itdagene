from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from itdagene.core.auth import set_current_user_function
from itdagene.core.models import Preference


class ForceDefaultLanguageMiddleware(MiddlewareMixin):
    """
    Ignore Accept-Language HTTP headers

    This will force the I18N machinery to always choose settings.LANGUAGE_CODE
    as the default initial language, unless another one is set via sessions or cookies

    Should be installed *before* any middleware that checks request.META['HTTP_ACCEPT_LANGUAGE'],
    namely django.middleware.locale.LocaleMiddleware
    """

    def process_request(self, request):
        if 'HTTP_ACCEPT_LANGUAGE' in request.META:
            del request.META['HTTP_ACCEPT_LANGUAGE']


class UnderDevelopmentMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path == reverse('itdagene.under_development') or 'login' in \
                request.path:
            return
        development = Preference.current_preference().development_mode
        if development:
            if request.user.is_authenticated:
                if not request.user.is_staff:
                    return HttpResponseRedirect(reverse('itdagene.under_development'))
            else:
                return HttpResponseRedirect(reverse('itdagene.under_development'))


class CurrentUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user = getattr(request, 'user', None)
        set_current_user_function(lambda: user)

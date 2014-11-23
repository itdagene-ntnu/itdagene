from itdagene.core.models import Preference
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse


class ForceDefaultLanguageMiddleware(object):
    """
    Ignore Accept-Language HTTP headers

    This will force the I18N machinery to always choose settings.LANGUAGE_CODE
    as the default initial language, unless another one is set via sessions or cookies

    Should be installed *before* any middleware that checks request.META['HTTP_ACCEPT_LANGUAGE'],
    namely django.middleware.locale.LocaleMiddleware
    """
    def process_request(self, request):
        if request.META.has_key('HTTP_ACCEPT_LANGUAGE'):
            del request.META['HTTP_ACCEPT_LANGUAGE']


class UnderDevelopmentMiddleware(object):
    def process_request(self, request):
        if request.path == reverse('itdagene.core.views.under_development') or 'login' in request.path: return
        development =  Preference.current_preference().development_mode
        if development:
            if request.user.is_authenticated():
                if not request.user.is_staff:
                    return HttpResponseRedirect(reverse('itdagene.core.views.under_development'))
            else:
                return HttpResponseRedirect(reverse('itdagene.core.views.under_development'))

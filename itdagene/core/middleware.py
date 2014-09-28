from django.conf import settings
from itdagene.core import Preference
from itdagene.core.shortcuts import Frontpage
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


def preprocessor(request):
    context = {}
    public = False
    pref = Preference.current_preference()
    context['pref'] = pref
    context['twitter'] = settings.VIEW_TWITTER_BOX

    if 'message' in request.session:
        if 'class' in request.session['message'] and 'value' in request.session['message']:
            context['message_class'] = request.session['message']['class']
            context['message_value'] = request.session['message']['value']
        del request.session['message']

    if not request.user.is_authenticated():
        public = True
    else:
        context['profile'] = request.user.profile

    if public:
        context['base_template'] = 'base_public.html'
        if not 'django_language' in request.session:
            request.session['django_language'] = 'nb'

        if not 'joblistings' in context:
            context['joblistings'] = Frontpage.public_joblistings()
        else:
            context['hide_joblistings_sidebar'] = True

    else:
        context['base_template'] = 'base.html'
    return context


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

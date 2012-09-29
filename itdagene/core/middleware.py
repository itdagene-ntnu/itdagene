from django.conf import settings
from itdagene.core import Preference
from itdagene.core.shortcuts import Frontpage

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
        if not request.session['django_language']: request.session['django_language'] = 'nb'
        if not context.has_key('joblistings'): context['joblistings'] = Frontpage.public_joblistings()
        else: context['hide_joblistings_sidebar'] = True
        request.session['django_language'] = 'nb'
    else:
        context['base_template'] = 'base.html'
    return context

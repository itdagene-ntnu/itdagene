from django.conf import settings
from itdagene.core.models import Preference


def site_processor(request):
    """
    Return site information in templates.
    """
    context = {}
    context['site'] = settings.SITE

    return context


def utils_processor(request):
    """
    Return site information in templates.
    """
    context = {}
    context['preferences'] = Preference.current_preference()

    return context

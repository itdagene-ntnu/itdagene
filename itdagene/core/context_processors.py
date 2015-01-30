from django.conf import settings
from itdagene.core.models import Preference
from itdagene.core.twitter import get_latest_tweet
from itdagene.core.instagram_helper import get_tag_images


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


def twitter(request):
    """
    Get the latest tweet as text.
    """
    context = {}
    context['tweet'] = get_latest_tweet()

    return context


def instagram(request):
    """
    Return a list og the 9 latest instagram images
    """
    return {'instagram': get_tag_images()}

from django.conf import settings

def site_processor(request):
    """
    Return site information in templates.
    """
    context = {}
    context['site'] = settings.SITE

    return context
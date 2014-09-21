from django.template import Library
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

register = Library()

@register.inclusion_tag('core/menu.html')
def menu(request):
    menu = [
            {'title': _('Home'), 'url': reverse('frontpage')},
            {'title': _('Program'), 'url': reverse('itdagene.app.events.views.public_event_list')},
            {'title': _('About itDAGENE'), 'url': reverse('itdagene.app.pages.views.view_page', args=['om-oss'])},
            {'title': _('Joblistings'), 'url': reverse('itdagene.app.career.views.joblistings.list_joblistings')},
            {'title': _('For attendees'), 'url': reverse('itdagene.app.pages.views.view_page', args=['for-bedrifter'])},
            {'title': _('Attending companies'), 'url': reverse('itdagene.app.pages.views.view_page', args=['deltakende_bedrifter'])},
#            {'title': _('Login'), 'url': '/login/?next=/'},
    ]
    return {'menu': menu, 'request': request}

@register.simple_tag
def active(request, pattern):
    import re
    if len(pattern) > 1 and re.search(pattern, request.path):
        return " active "
    elif request.path == '/' and pattern == '/':
        return " active "
    return ""
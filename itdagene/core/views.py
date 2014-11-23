from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render
from itdagene.core.models import Preference


def error403(request):
    return render(request, 'static/403.html', {'title': _('Permission Denied')})


def error404(request):
    return render(request, 'static/404.html', {'title': _('Page not Found')})


def error500(request):
    return render(request, 'static/500.html', {'title': _('Internal Server Error')})


def under_development(request):
    year = Preference.current_preference().year
    return render(request, 'static/under_development.html', {'title': _('Under Development'),
                                                             'year': year})

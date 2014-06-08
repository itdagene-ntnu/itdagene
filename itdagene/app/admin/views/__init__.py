from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from itdagene.core.util.cache import get_stats

from itdagene.core.log.models import LogItem


@permission_required('log.change_log')
def landing_page(request):
    return render(request, 'adm/dashboard.html', {'cache_stats': get_stats()})


@permission_required('log.change_log')
def log(request, first_object=0):
    if int(first_object) > 40:
        previous = int(first_object) - 40
    else:
        previous = None

    log = LogItem.objects.all().select_related('user', 'content_type', 'content_object').order_by('timestamp').reverse()[int(first_object):int(first_object) + 40]
    return render(request,'adm/log.html',
                             {'log': log,
                              'previous': previous,
                              'next': int(first_object) + 41})
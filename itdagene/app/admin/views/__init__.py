from django.contrib.auth.decorators import login_required, permission_required
from itdagene.core.log.models import LogItem
from itdagene.core.profiles.models import Profile
from django.shortcuts import render

@permission_required('log.change_log')
def landing_page (request):
    count = Count
    return render(request,'adm/base.html',
                             {'count': count})

@permission_required('log.change_log')
def log (request, first_object=0):
    if int(first_object) > 40: previous = int(first_object) - 40
    else: previous = None

    log = LogItem.objects.all().select_related('user','content_type', 'content_object').order_by('timestamp').reverse()[int(first_object):int(first_object) + 40]
    return render(request,'adm/log.html',
                             {'log': log,
                              'previous': previous,
                              'next': int(first_object) + 41})


class Count:
    def b(self): return Profile.get_count_for_type('b')
    def c(self): return Profile.get_count_for_type('c')
    def u(self): return Profile.get_count_for_type('u')
    def w(self): return Profile.get_count_for_type('w')
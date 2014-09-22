# -*- coding: utf-8 -*-
from django.http import Http404
from django.utils.translation import ugettext_lazy as _
from itdagene.app.api.util import render_json, login_or_token_required
from itdagene.app.workschedule.models import Worker

def get(request, username):
    try:
        worker = Worker.objects.get(username=username)

        return render_json({
            'worker': worker.as_dict(),
            'schedules': [schedule.as_dict() for schedule in worker.in_schedules.all()]
        })

    except (Worker.DoesNotExist):
        return render_json(error='Could not find worker')

def list(request):

    if not request.GET.get('token') == 'jtQu6iPH3WhQLH':
        raise Http404

    worker_list = []

    for worker in Worker.objects.all():
        has_met = True

        if worker.in_schedules.all().count():
            for schedule in worker.in_schedules.all():
                if not schedule.has_met:
                    has_met = False
        else:

            has_met = False


        worker_list.append({
            'username': worker.username,
            'name': unicode(worker.name),
            'has_met': has_met
        })

    return render_json(worker_list)
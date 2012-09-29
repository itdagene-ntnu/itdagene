# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from itdagene.api.util import render_json, login_or_token_required
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

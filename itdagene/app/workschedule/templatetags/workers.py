from datetime import datetime
from django.template.base import Library
from itdagene.app.workschedule.models import WorkSchedule

register = Library()

@register.inclusion_tag('workschedule/current_workers.html')
def current_workers():
    workschedule = WorkSchedule.objects.filter(start_time__lt=datetime.now(), end_time__gt=datetime.now())
    return {'workschedule': workschedule}

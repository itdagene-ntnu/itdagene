from django.forms.models import ModelForm
from itdagene.app.workschedule.models import WorkSchedule
from django.contrib.auth.models import User

class WorkScheduleForm (ModelForm):

    class Meta:
        model = WorkSchedule

    def __init__(self, *args, **kwargs):
        super(WorkScheduleForm, self).__init__(*args, **kwargs)
        users = User.objects.filter(is_active=True, profile__type='w').order_by('first_name')
        self.fields['contact'].choices = [(user.pk, user.get_full_name()) for user in users]
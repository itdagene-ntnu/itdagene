from django import forms
from django.forms.models import ModelForm
from django.utils.translation import gettext_lazy as _

from itdagene.app.workschedule.models import Worker, WorkerInSchedule, WorkSchedule
from itdagene.core.models import Preference


class WorkScheduleForm(ModelForm):
    invites = forms.MultipleChoiceField(label=_("Add worker"), required=False)

    class Meta:
        model = WorkSchedule
        fields = ("title", "date", "start_time", "end_time", "description", "invites")

    def __init__(self, *args, **kwargs):
        super(WorkScheduleForm, self).__init__(*args, **kwargs)
        workers = Worker.objects.filter(
            preference=Preference.current_preference().year
        ).order_by("name")
        self.fields["invites"].choices = [
            (worker.pk, worker.name) for worker in workers
        ]
        self.fields["invites"].widget.attrs["class"] = "chosen"

    def save(self, commit=True):
        workschedule = super(WorkScheduleForm, self).save(commit=commit)

        for i in self.cleaned_data["invites"]:
            WorkerInSchedule.objects.get_or_create(schedule=workschedule, worker_id=i)

        return workschedule


class WorkerForm(ModelForm):
    class Meta:
        model = Worker
        fields = ("name", "phone", "email", "t_shirt_size")

    def __init__(self, *args, **kwargs):
        super(WorkerForm, self).__init__(*args, **kwargs)

    def save(self):
        pref = Preference.current_preference()
        worker = super(WorkerForm, self).save(commit=False)
        worker.preference = pref.year
        worker.save()
        return worker

from django.forms.models import ModelForm
from itdagene.core import Preference
from django.utils.translation import ugettext_lazy as _
from django import forms
from itdagene.app.workschedule.models import WorkSchedule, Worker, WorkerInSchedule
from django.contrib.auth.models import User

class WorkScheduleForm (ModelForm):
	invites = forms.MultipleChoiceField(label='Add worker', required=False)

	class Meta:
		model = WorkSchedule

	def __init__(self, *args, **kwargs):
		super(WorkScheduleForm, self).__init__(*args, **kwargs)
		workers = Worker.objects.all().order_by('name')
		self.fields['invites'].choices = [(worker.pk, worker.name) for worker in workers]
		self.fields['invites'].widget.attrs['class'] = 'chosen'

	def save(self, commit=True):
		pref = Preference.current_preference()
		workschedule = super(WorkScheduleForm, self).save(commit=commit)

		for i in self.cleaned_data['invites']:
			WorkerInSchedule.objects.get_or_create(schedule=workschedule, worker_id=i)

		return workschedule

class WorkerForm(ModelForm):

	class Meta:
		model = Worker

	def __init__(self, *args, **kwargs):
		super(WorkerForm, self).__init__(*args, **kwargs)

	def save(self, commit=True):
		pref = Preference.current_preference()
		worker = super(WorkerForm, self).save(commit=commit)

		return worker
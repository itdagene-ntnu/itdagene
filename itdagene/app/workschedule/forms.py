from django.forms.models import ModelForm
from django.forms.forms import Form
from itdagene.core import Preference
from django.utils.translation import ugettext_lazy as _
from django import forms
from itdagene.app.workschedule.models import WorkSchedule, Worker, WorkerInSchedule
from itdagene.core.models import User


class WorkScheduleForm (ModelForm):
	invites = forms.MultipleChoiceField(label=_('Add worker'), required=False)

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

class WorkerHasMetForm(ModelForm):
	schedule = forms.IntegerField(label=_('Task'), widget=forms.HiddenInput())
	attendance = forms.MultipleChoiceField(label=_('Has Met'), required=False)

	class Meta:
		model = WorkerInSchedule
		exclude = ('worker', 'has_met', 'schedule')

	def __init__(self, *args, **kwargs):
		task = kwargs.pop('task', None)
		super(WorkerHasMetForm, self).__init__(*args, **kwargs)
		self.fields['attendance'].choices = [(worker.pk, worker) for worker in task.workers()]
		self.fields['attendance'].widget.attrs['class'] = 'chosen'

	def save(self, commit=True):
		workerHasMet = super(WorkerHasMetForm, self)
		schedule = self.cleaned_data['schedule']

		for i in self.cleaned_data['attendance']:
			worker = WorkerInSchedule.objects.get(worker_id=i, schedule=schedule)
			worker.has_met = True
			worker.save()

		return workerHasMet
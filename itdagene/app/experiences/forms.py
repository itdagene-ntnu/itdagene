from django.forms.models import ModelForm
from django.forms.forms import Form
from itdagene.core import Preference
from django.utils.translation import ugettext_lazy as _
from django import forms
from itdagene.app.experiences.models import Experience

class ExperienceForm(ModelForm):
	class Meta:
		model = Experience
		exclude = ('year', 'last_updated')

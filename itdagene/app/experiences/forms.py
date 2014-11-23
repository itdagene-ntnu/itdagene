from django.forms.models import ModelForm
from itdagene.app.experiences.models import Experience


class ExperienceForm(ModelForm):
    class Meta:
        model = Experience
        exclude = ('year', 'last_updated')

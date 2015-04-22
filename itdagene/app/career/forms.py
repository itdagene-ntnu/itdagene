from django.forms.models import ModelForm

from itdagene.app.career.models import Joblisting, Town


class JoblistingForm(ModelForm):
    class Meta:
        model = Joblisting
        fields = (
            'title',
            'type',
            'company',
            'description',
            'contact',
            'deadline',
            'from_year',
            'to_year',
            'url',
            'towns',
            'image',
            'frontpage')


class JoblistingTownForm(ModelForm):
    class Meta:
        model = Town

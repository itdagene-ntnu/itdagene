from django.forms.models import ModelForm
from itdagene.app.venue.models import Stand
from itdagene.core.models import BaseModel

class StandForm(ModelForm):
    class Meta:
        model=Stand
        exclude = BaseModel.exclude_fields()
from django.forms.models import ModelForm
from itdagene.app.venue.models import Stand, StandCompany
from itdagene.core.models import BaseModel


class StandForm(ModelForm):
    class Meta:
        model = Stand
        exclude = BaseModel.exclude_fields()


class StandCompanyForm(ModelForm):
    class Meta:
        model = StandCompany
        exclude = ('company', )

from django.forms.models import ModelForm
from itdagene.app.career.models import Joblisting
from itdagene.app.company.models import CompanyContact

class JoblistingForm (ModelForm):

    def __init__(self,*args,**kwargs):
        super (JoblistingForm,self).__init__(*args,**kwargs)
        self.fields['contact'].queryset = CompanyContact.objects.filter(company=self.instance.company)

    class Meta:
        model = Joblisting
        fields = (
            'title',
            'type',
            'description',
            'contact',
            'deadline',
            'from_year',
            'to_year',
            'url',
            'towns',
            'image')


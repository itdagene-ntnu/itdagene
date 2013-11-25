from django.forms.models import ModelForm
from itdagene.app.career.models import Joblisting
from itdagene.app.company.models import CompanyContact
from django.utils.translation import ugettext_lazy as _


class JoblistingForm (ModelForm):
    title = _('Add joblisting')
    keyword = 'joblisting'

    def __init__(self, *args, **kwargs):
        super(JoblistingForm,self).__init__(*args, **kwargs)
        self.fields['contact'].queryset = CompanyContact.objects.filter(company=self.instance)

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


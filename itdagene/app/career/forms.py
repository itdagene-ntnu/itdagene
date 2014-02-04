from django.forms.models import ModelForm
from itdagene.app.career.models import Joblisting
from itdagene.app.company.models import CompanyContact
from django.utils.translation import ugettext_lazy as _


class JoblistingForm(ModelForm):
    form_title = _('Add joblisting')
    keyword = 'joblisting'
    action_url = 'careers/joblistings/add/'

    def __init__(self, *args, **kwargs):
        super(JoblistingForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            if field.widget.is_required:
                field.widget.attrs['required'] = 'required'
        self.fields['contact'].queryset = CompanyContact.objects.filter(company=self.instance)
        self.action_url += str(self.instance.pk) + '/'
        self.fields['deadline'].widget.attrs['placeholder'] = 'YYYY-MM-DD'

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


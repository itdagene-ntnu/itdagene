from itdagene.app.company.models import Company, Comment, Package, CompanyContact, Contract
from django.forms.models import ModelForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from itdagene.app.company import COMPANY_STATUS


class PackageForm(ModelForm):
    form_title = _('Add package')
    keyword = 'package'
    action_url = '/bdb/packages/add'

    class Meta:
        model = Package
        exclude = ('is_full',)


class CompanyForm(ModelForm):
    form_title = _('Add company')
    keyword = 'company'
    action_url = '/bdb/companies/add/'

    class Meta:
        model = Company
        exclude = ('package',)

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            if field.widget.is_required:
                field.widget.attrs['required'] = 'required'
        users = User.objects.filter(is_active=True, profile__type='b').order_by('first_name')
        self.fields['contact'].choices = [('', '----')] + [(user.pk, user.get_full_name()) for user in users]
        waiting_lists = Package.objects.filter(is_full=True, has_waiting_list=True)
        self.fields['waiting_for_package'].queryset = waiting_lists


class BookCompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ('package',)

    def __init__(self, *args, **kwargs):
        super(BookCompanyForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            if field.widget.is_required:
                field.widget.attrs['required'] = 'required'
        packages = Package.objects.filter(is_full=False)
        self.fields['package'].queryset = packages
        

class WaitingListCompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ('waiting_for_package',)

    def __init__(self, *args, **kwargs):
        super(WaitingListCompanyForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            if field.widget.is_required:
                field.widget.attrs['required'] = 'required'
        waiting_lists = Package.objects.filter(is_full=True, has_waiting_list=True)
        self.fields['waiting_for_package'].queryset = waiting_lists


class ResponsibilityForm(ModelForm):
    class Meta:
        model = Company
        fields = ('contact',)

    def __init__(self, *args, **kwargs):
        super(ResponsibilityForm, self).__init__(*args, **kwargs)
        users = User.objects.filter(is_active=True, profile__type='b').order_by('first_name')
        self.fields['contact'].choices = [('', '----')] + [(user.pk, user.get_full_name()) for user in users]


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('content', 'company')


class CompanyContactForm(ModelForm):
    form_title = _('ADD CONTACT')
    keyword = 'company_contact'
    action_url = ''

    class Meta:
        model = CompanyContact
        exclude = ('company',)

    def __init__(self, *args, **kwargs):
        super(CompanyContactForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            if field.widget.is_required:
                field.widget.attrs['required'] = 'required'
        self.action_url = '/bdb/contacts/' + str(self.instance.pk) + '/add/'


class CompanyStatusForm(ModelForm):
    class Meta:
        model = Company
        fields = ('status',)

    def __init__(self, *args, **kwargs):
        super(CompanyStatusForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            if field.widget.is_required:
                field.widget.attrs['required'] = 'required'
        self.fields['status'].choices = list(COMPANY_STATUS)


class ContractForm(ModelForm):
    form_title = _('ADD CONTRACT')
    keyword = 'contract'
    action_url = ''

    class Meta:
        model = Contract
        exclude = ('company', 'banquet_tickets')

    def __init__(self, *args, **kwargs):
        super(ContractForm, self).__init__(*args, **kwargs)
        for _, field in self.fields.items():
            if field.widget.is_required:
                field.widget.attrs['required'] = 'required'
        self.action_url = '/bdb/contracts/' + str(self.instance.pk) + '/add/'
        self.fields['timestamp'].widget.attrs['placeholder'] = 'YYYY-MM-DD'
from itdagene.app.company.models import Company, Comment, Package, CompanyContact, Contract
from django.forms.models import ModelForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class PackageForm(ModelForm):
    class Meta:
        model = Package
        exclude = ('is_full')


class CompanyForm(ModelForm):
    form_title = _('Add company')
    keyword = 'company'
    action_url = '/bdb/companies/add/'

    class Meta:
        model = Company
        exclude = ('package')

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        users = User.objects.filter(is_active=True, profile__type='b').order_by('first_name')
        self.fields['contact'].choices = [('', '----')] + [(user.pk, user.get_full_name()) for user in users]
        waiting_lists = Package.objects.filter(is_full=True, has_waiting_list=True)
        self.fields['waiting_for_package'].queryset = waiting_lists


class BookCompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ('package', 'waiting_for_package')

    def __init__(self, *args, **kwargs):
        super(BookCompanyForm, self).__init__(*args, **kwargs)
        packages = Package.objects.filter(is_full=False)
        self.fields['package'].queryset = packages
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
        exclude = ('company')

    def __init__(self, *args, **kwargs):
        super(CompanyContactForm, self).__init__(*args, **kwargs)
        self.url = '/bdb/contacts/' + str(self.instance.pk) + '/add/'


class ContractForm(ModelForm):
    form_title = _('ADD CONTRACT')
    keyword = 'contract'
    action_url = ''

    class Meta:
        model = Contract
        exclude = ('company', 'banquet_tickets')

    def __init__(self, *args, **kwargs):
        super(ContractForm, self).__init__(*args, **kwargs)
        self.url = '/bdb/contracts/' + str(self.instance.pk) + '/add/'
        self.fields['timestamp'].widget.attrs['placeholder'] = 'YYYY-MM-DD HH:MM'
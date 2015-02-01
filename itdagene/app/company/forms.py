from itdagene.app.company.models import Company, Package, CompanyContact, Contract
from django.forms.models import ModelForm
from itdagene.core.models import User
from django.utils.translation import ugettext_lazy as _
from itdagene.app.company import COMPANY_STATUS
from itdagene.core.models import Preference
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit
from crispy_forms.bootstrap import FieldWithButtons, StrictButton
from django.db.models import Q


class PackageForm(ModelForm):
    keyword = 'package'
    action_url = '/bdb/packages/add'

    class Meta:
        model = Package
        exclude = ('is_full',)


class CompanyForm(ModelForm):
    keyword = 'company'
    action_url = '/bdb/companies/add/'

    class Meta:
        model = Company
        exclude = ('package', 'active')

    def __init__(self, *args, **kwargs):
        super(CompanyForm, self).__init__(*args, **kwargs)
        users = User.objects.filter(is_active=True, is_staff=True, year=Preference.current_preference().year).order_by('first_name')
        self.fields['contact'].choices = [('', '----')] + [(user.pk, user.get_full_name()) for user in users]
        waiting_lists = Package.objects.filter(is_full=True, has_waiting_list=True)
        self.fields['waiting_for_package'].queryset = waiting_lists


class BookCompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ('package',)

    def __init__(self, *args, **kwargs):
        super(BookCompanyForm, self).__init__(*args, **kwargs)
        packages = Package.objects.filter(Q(is_full=False) or Q(companies=self.instance))
        self.fields['package'].queryset = packages

        self.helper = FormHelper()
        self.helper.layout = Layout(
            FieldWithButtons('package', StrictButton(_('Save'), type='submit', css_class='btn-success'))
        )




class WaitingListCompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ('waiting_for_package',)

    def __init__(self, *args, **kwargs):
        super(WaitingListCompanyForm, self).__init__(*args, **kwargs)
        waiting_lists = Package.objects.filter(is_full=True, has_waiting_list=True).exclude(companies=self.instance)
        self.fields['waiting_for_package'].queryset = waiting_lists
        self.fields['waiting_for_package'].help_text = None

        self.helper = FormHelper()
        self.helper.layout = Layout(
            FieldWithButtons('waiting_for_package', StrictButton(_('Save'), type='submit', css_class='btn-success'))
        )


class ResponsibilityForm(ModelForm):
    class Meta:
        model = Company
        fields = ('contact',)

    def __init__(self, *args, **kwargs):
        super(ResponsibilityForm, self).__init__(*args, **kwargs)
        users = User.objects.filter(is_active=True, is_staff=True, year=Preference.current_preference().year).order_by('first_name')
        self.fields['contact'].choices = [('', '----')] + [(user.pk, user.get_full_name()) for user in users]


class CompanyContactForm(ModelForm):
    keyword = 'company_contact'
    action_url = ''

    class Meta:
        model = CompanyContact
        exclude = ('company',)

    def __init__(self, *args, **kwargs):
        super(CompanyContactForm, self).__init__(*args, **kwargs)
        self.action_url = '/bdb/contacts/' + str(self.instance.pk) + '/add/'


class CompanyStatusForm(ModelForm):
    class Meta:
        model = Company
        fields = ('status',)

    def __init__(self, *args, **kwargs):
        super(CompanyStatusForm, self).__init__(*args, **kwargs)
        self.fields['status'].choices = list(COMPANY_STATUS)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            FieldWithButtons('status', StrictButton(_('Save'), type='submit', css_class='btn-success'))
        )


class ContractForm(ModelForm):
    keyword = 'contract'

    class Meta:
        model = Contract
        fields = ('timestamp', 'file', 'joblistings', 'interview_room', 'is_billed', 'has_paid')

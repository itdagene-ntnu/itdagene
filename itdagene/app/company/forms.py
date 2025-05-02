from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.db.models import Q
from django.forms.models import ModelForm

from itdagene.app.company import COMPANY_STATUS
from itdagene.app.company.models import (
    Company,
    CompanyContact,
    Contract,
    KeyInformation,
    Package,
)
from itdagene.core.models import Preference, User


class PackageForm(ModelForm):
    keyword = "package"
    action_url = "/bdb/packages/add"

    class Meta:
        model = Package
        exclude = ("is_full",)


class CompanyForm(ModelForm):
    keyword = "company"
    action_url = "/bdb/companies/add/"

    class Meta:
        model = Company
        exclude = ("package", "active")

    def __init__(self, *args, **kwargs) -> None:
        super(CompanyForm, self).__init__(*args, **kwargs)
        users = User.objects.filter(
            is_active=True, is_staff=True, year=Preference.current_preference().year
        ).order_by("first_name")
        self.fields["contact"].choices = [("", "----")] + [
            (user.pk, user.get_full_name()) for user in users
        ]
        waiting_lists = Package.objects.filter(is_full=True, has_waiting_list=True)
        self.fields["waiting_for_package"].queryset = waiting_lists


class ResponsibilityForm(ModelForm):
    class Meta:
        model = Company
        fields = ("contact",)

    def __init__(self, *args, **kwargs) -> None:
        super(ResponsibilityForm, self).__init__(*args, **kwargs)
        users = User.objects.filter(
            is_active=True, is_staff=True, year=Preference.current_preference().year
        ).order_by("first_name")
        self.fields["contact"].choices = [("", "----")] + [
            (user.pk, user.get_full_name()) for user in users
        ]


class CompanyContactForm(ModelForm):
    keyword = "company_contact"
    action_url = ""

    class Meta:
        model = CompanyContact
        exclude = ("company",)

    def __init__(self, *args, **kwargs) -> None:
        super(CompanyContactForm, self).__init__(*args, **kwargs)
        self.action_url = "/bdb/contacts/" + str(self.instance.pk) + "/add/"


class CompanyPackageForm(ModelForm):
    class Meta:
        model = Company
        fields = ("package", "status", "waiting_for_package")

    def __init__(self, *args, **kwargs) -> None:
        super(CompanyPackageForm, self).__init__(*args, **kwargs)

        packages = Package.objects.filter(Q(is_full=False) | Q(companies=self.instance))
        waiting_for_package = Package.objects.filter(
            Q(is_full=True) & Q(has_waiting_list=True)
        ).exclude(companies=self.instance)

        self.fields["package"].queryset = packages
        self.fields["waiting_for_package"].queryset = waiting_for_package
        self.fields["status"].choices = list(COMPANY_STATUS)

        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Lagre", css_class="btn btn-success"))


class ContractForm(ModelForm):
    keyword = "contract"

    class Meta:
        model = Contract
        fields = (
            "timestamp",
            "file",
            "joblistings",
            "interview_room",
            "is_billed",
            "has_paid",
        )


class KeyInformationForm(ModelForm):
    keyword = "key_information"
    action_url = ""

    class Meta:
        model = KeyInformation
        fields = ("name", "value")

    def __init__(self, *args, **kwargs) -> None:
        super(KeyInformationForm, self).__init__(*args, **kwargs)
        self.action_url = "/bdb/key_information/" + str(self.instance.pk) + "/add/"

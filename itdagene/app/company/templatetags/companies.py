from django.template import Library

from itdagene.app.company.forms import (
    BookCompanyForm,
    CompanyStatusForm,
    WaitingListCompanyForm,
)


register = Library()


@register.inclusion_tag("company/templatetags/book_form.html")
def book_form(company) -> dict:
    form = BookCompanyForm(instance=company)
    return {"form": form}


@register.inclusion_tag("company/templatetags/waiting_list_form.html")
def waiting_list_form(company) -> dict:
    form = WaitingListCompanyForm(instance=company)
    return {"form": form}


@register.inclusion_tag("company/templatetags/status_form.html")
def status_form(company) -> dict:
    form = CompanyStatusForm(instance=company)
    return {"form": form}

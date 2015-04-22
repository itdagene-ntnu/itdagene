from django.template.base import Library

from itdagene.app.company.forms import BookCompanyForm, CompanyStatusForm, WaitingListCompanyForm

register = Library()


@register.inclusion_tag('company/templatetags/book_form.html')
def book_form(company):
    form = BookCompanyForm(instance=company)
    return {'form': form}


@register.inclusion_tag('company/templatetags/waiting_list_form.html')
def waiting_list_form(company):
    form = WaitingListCompanyForm(instance=company)
    return {'form': form}


@register.inclusion_tag('company/templatetags/status_form.html')
def status_form(company):
    form = CompanyStatusForm(instance=company)
    return {'form': form}

from django.template.base import Library
from itdagene.app.company.forms import BookCompanyForm, CompanyStatusForm, WaitingListCompanyForm
from itdagene.core.models import Preference
from django.utils.translation import ugettext as _

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

@register.simple_tag
def feedback_overview():
    return '''<li><a href="/feedback/report/%d/" >%s</a></li>''' % ((Preference.current_preference().year -1), _("FEEDBACK OVERVIEW"))
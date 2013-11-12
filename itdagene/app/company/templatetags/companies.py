from django.template.base import Library
from itdagene.app.company.forms import BookCompanyForm

register = Library()

@register.inclusion_tag('company/templatetags/book_form.html')
def book_form(company):
    form = BookCompanyForm(instance=company)
    return {'form': form}

from django.template.base import Library
from itdagene.app.company.forms import CommentForm, BookCompanyForm
from itdagene.app.company.models import Comment

register = Library()

@register.inclusion_tag('company/templatetags/book_form.html')
def book_form(company):
    form = BookCompanyForm(instance=company)
    return {'form': form}

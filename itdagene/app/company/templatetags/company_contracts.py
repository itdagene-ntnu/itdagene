from django.template.base import Library
from itdagene.app.company.forms import ContractForm
from itdagene.app.company.models import Contract

register = Library()

@register.inclusion_tag('company/contracts/form.html')
def contract_form(company):
    form = ContractForm(instance=Contract(company=company))
    return {'form': form, 'company': company}

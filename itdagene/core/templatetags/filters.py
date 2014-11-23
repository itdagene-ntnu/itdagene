from django.template.base import Library
from django.utils import formats
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

register = Library()


@register.filter
def boolean(value, arg=None):
    """
    Returns HTML markup for a Glyphicon based on the truthiness of the value
    """
    if value:
        return mark_safe('<span class="glyphicon glyphicon-ok" alt="yes">')
    return mark_safe('<span class="glyphicon glyphicon-remove" alt="no">')


@register.filter
def has_contract_for_current_year(value, arg=None):
    """
    Returns True if the contract passed as value is from current year
    """
    from itdagene.core.models import Preference
    for contract in value:
        if contract.timestamp.year == Preference.current_preference().year:
            return True
    return False

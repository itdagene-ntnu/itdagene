from django.core import cache
from django.template.base import Library
from itdagene.core.forms import ProfileSearchForm

register = Library()

@register.inclusion_tag('core/profile/search.html')
def search(request):
    search_form = ProfileSearchForm()
    return {'search_form': search_form}
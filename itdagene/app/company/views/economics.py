from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

from itdagene.app.company.models import Company


@permission_required('company.change_contract')
def economic_overview(request):
    companies = Company.objects.filter(active=True,
                                       status=3).exclude(
                                           contracts=None).select_related()
    return render(request, 'company/economics/base.html',
                  {'companies': companies,
                   'title': _('Economic Overview')})

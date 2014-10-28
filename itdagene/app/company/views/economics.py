from django.http import HttpResponse
from itdagene.app.company.models import Company, Contract
from django.contrib.auth.decorators import permission_required
from django.views.decorators.http import require_GET, require_POST
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _


@permission_required('company.change_contract')
def economic_overview(request):
    companies = Company.objects.filter(active=True, status=3).exclude(contracts=None).select_related()
    return render(request, 'company/economics/base.html',
                  {'companies': companies, 'title': _('Economic Overview')})

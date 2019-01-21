from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from itdagene.app.company.models import Company


@permission_required("company.change_contract")
def economic_overview(request):
    all_companies = (
        Company.objects.filter(active=True, status=3)
        .exclude(contracts=None)
        .select_related()
    )
    companies = []
    for company in all_companies:
        if company.current_contract():
            companies.append(company)
    return render(
        request,
        "company/economics/base.html",
        {"companies": companies, "title": _("Economic Overview")},
    )

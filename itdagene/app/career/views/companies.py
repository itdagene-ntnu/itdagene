from django.utils.datetime_safe import datetime
from itdagene.app.company.models import Company
from django.shortcuts import render
from django.shortcuts import get_object_or_404

def company_profile(request, id):
    company = get_object_or_404(Company.objects.select_related(), pk=id)
    joblistings = list(company.joblistings.filter(deadline__gt=datetime.now(), company=company))
    joblistings += list(company.joblistings.filter(deadline=None, company=company))
    return render(request, 'career/companies/view.html', {
        'company': company,
        'joblistings': joblistings,
    })
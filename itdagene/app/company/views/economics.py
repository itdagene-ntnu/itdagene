from django.http import HttpResponse
from itdagene.app.company.models import Company, Contract
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

@permission_required('company.change_contract')
def economic_overview (request):
    companies = Company.objects.filter(active=True, status=3).exclude(contracts=None).select_related()
    return render(request, 'company/economics/base.html',
            {'companies': companies})

@permission_required('company.change_contract')
def billed (request, company_id):
    c = Company.objects.get(pk=company_id).current_contract()
    c.is_billed = True
    c.save()
    return HttpResponse()

@permission_required('company.change_contract')
def not_billed (request, company_id):
    c = Company.objects.get(pk=company_id).current_contract()
    c.is_billed = False
    c.save()
    return HttpResponse()

@permission_required('company.change_contract')
def paid (request, company_id):
    c = Company.objects.get(pk=company_id).current_contract()
    c.has_paid = True
    c.save()
    return HttpResponse()

@permission_required('company.change_contract')
def not_paid (request, company_id):
    c = Company.objects.get(pk=company_id).current_contract()
    c.has_paid = False
    c.save()
    return HttpResponse()
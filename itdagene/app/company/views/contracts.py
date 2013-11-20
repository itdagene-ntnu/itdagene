from django.core.urlresolvers import reverse
from itdagene.app.company.forms import ContractForm
from itdagene.app.company.models import Contract, Company
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, HttpResponse


@permission_required('company.change_contract')
def edit_contract(request, company_id, id=False):
    company = get_object_or_404(Company, pk=company_id)
    contract = Contract(company=company)
    if id:
        contract = get_object_or_404(Contract, pk=id)
        if not contract.company == company:
            raise Http404
    form = ContractForm(instance=contract)
    if request.method == 'POST':
        form = ContractForm(request.POST, request.FILES, instance=contract)
        if form.is_valid():
            contract = form.save()
            return redirect(contract.company.get_absolute_url())
    return redirect(company.get_absolute_url())
    #return render(request, 'company/contracts/form.html', {'form': form, 'company': company})


@permission_required('company.change_contract')
def download_contract(request, company_id, id):
    import os
    contract = get_object_or_404(Contract,pk=id, company__id=company_id)
    abspath = open(contract.file.path,'r')
    response = HttpResponse(content=abspath.read())
    response['Content-Type']= 'application/octet-stream'
    response['Content-Disposition'] = 'attachment; filename=%s'\
    % os.path.basename(contract.file.path)
    return response
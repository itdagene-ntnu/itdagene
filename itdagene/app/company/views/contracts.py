import os
from typing import Any

from django.contrib.auth.decorators import permission_required
from django.contrib.messages import SUCCESS, add_message
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _

from itdagene.app.company.forms import ContractForm
from itdagene.app.company.models import Company, Contract
from itdagene.core.decorators import staff_required


@permission_required("company.add_contract")
def add_contract(request: HttpRequest, company_id: Any) -> HttpResponse:
    company = get_object_or_404(Company, pk=company_id)
    form = ContractForm()
    if request.method == "POST":
        form = ContractForm(request.POST, request.FILES)
        if form.is_valid():
            contract = form.save(commit=False)
            contract.company = company
            contract.save()
            add_message(request, SUCCESS, _("Contract added."))
            return redirect(company.get_absolute_url())
    return render(
        request,
        "company/form.html",
        {"title": _("Add Contract"), "form": form, "company": company},
    )


@permission_required("company.change_contract")
def edit_contract(request: HttpRequest, company_id: Any, id: Any) -> HttpResponse:
    company = get_object_or_404(Company, pk=company_id)
    contract = get_object_or_404(Contract, pk=id)
    if contract.company != company:
        raise Http404

    form = ContractForm(instance=contract)
    if request.method == "POST":
        form = ContractForm(request.POST, request.FILES, instance=contract)
        if form.is_valid():
            form.save()
            return redirect(company.get_absolute_url())
    return render(
        request,
        "company/form.html",
        {
            "form": form,
            "company": company,
            "title": _("Change Contract"),
            "description": contract,
        },
    )


@staff_required()
def download_contract(request: Any, company_id: Any, id: Any) -> HttpResponse:
    contract = get_object_or_404(Contract, pk=id, company__id=company_id)
    abspath = open(contract.file.path, "rb")
    response = HttpResponse(content=abspath.read())
    response["Content-Type"] = "application/octet-stream"
    response[
        "Content-Disposition"
    ] = f"attachment; filename={os.path.basename(contract.file.path)}"
    return response


@permission_required("company.delete_contract")
def delete_contract(request: HttpRequest, company_id: Any, id: Any) -> HttpResponse:
    company = get_object_or_404(Company, pk=company_id)
    contract = get_object_or_404(Contract, pk=id)
    if contract.company != company:
        raise Http404

    if request.method == "POST":
        contract.delete()
        return redirect(company.get_absolute_url())
    return render(
        request,
        "company/contracts/delete.html",
        {
            "contract": contract,
            "company": contract.company,
            "title": _("Delete Contract"),
            "description": contract,
        },
    )

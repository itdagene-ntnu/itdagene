from django.contrib.auth.decorators import permission_required
from django.contrib.messages import SUCCESS, add_message
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from itdagene.app.company.forms import CompanyContactForm
from itdagene.app.company.models import Company, CompanyContact
from itdagene.core import vcard_string
from itdagene.core.decorators import staff_required


@permission_required("company.add_companycontact")
def add_contact(request, company):
    company = get_object_or_404(Company, pk=company)
    form = CompanyContactForm()
    if request.method == "POST":
        form = CompanyContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.company = company
            contact.phone = contact.phone.replace(" ", "") if contact.phone else None
            contact.mobile_phone = (
                contact.mobile_phone.replace(" ", "") if contact.mobile_phone else None
            )
            contact.email = contact.email.lower() if contact.email else None
            contact.save()
            return redirect(company.get_absolute_url())
    return render(
        request,
        "company/form.html",
        {
            "title": _("Add Contact"),
            "description": company,
            "form": form,
            "company": company,
        },
    )


@permission_required("company.delete_companycontact")
def delete_contact(request, contact_id):
    contact = get_object_or_404(CompanyContact, pk=contact_id)
    company = contact.company
    if request.method == "POST":
        contact.delete()
        return redirect(company.get_absolute_url())
    else:
        return render(
            request,
            "company/contacts/delete.html",
            {
                "contact": contact,
                "company": contact.company,
                "title": _("Delete Contact"),
                "description": contact,
            },
        )


@permission_required("company.change_companycontact")
def edit_contact(request, contact_id):
    contact = get_object_or_404(CompanyContact, pk=contact_id)
    form = CompanyContactForm(instance=contact)

    if request.method == "POST":
        form = CompanyContactForm(request.POST, instance=contact)
        if form.is_valid():
            contact = form.save()
            add_message(request, SUCCESS, _("Company contect saved."))
            return redirect(reverse("itdagene.company.view", args=[contact.company.pk]))

    return render(
        request,
        "company/form.html",
        {
            "form": form,
            "company": contact.company,
            "title": _("Change Contact"),
            "description": contact,
        },
    )


@staff_required()
def vcard(request, id):
    contact = get_object_or_404(CompanyContact, pk=id)
    person = Person()
    person.first_name = contact.first_name
    person.last_name = contact.last_name
    person.email = contact.email
    person.phone = contact.phone
    output = vcard_string(person)
    filename = "%s%s.vcf" % (person.first_name, person.last_name)
    response = HttpResponse(output, content_type="text/x-vCard")
    response["Content-Disposition"] = "attachment; filename=%s" % filename
    return response


class Person:
    def __init__(self):
        self.first_name = ""
        self.last_name = ""
        self.email = ""
        self.phone = ""

from datetime import datetime
from django.http import Http404, HttpResponse
from itdagene.app.company.forms import CommentForm, CompanyContactForm
from itdagene.app.company.models import Comment, CompanyContact, Company
from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import permission_required
from itdagene.core.profiles import _vcard_string
from django.shortcuts import render

@permission_required('company.change_companycontact')
def edit_contact (request, company_id=None, contact_id=None):
    form = None
    if contact_id:
        contact = get_object_or_404(CompanyContact, pk=contact_id)
        form = CompanyContactForm(instance=contact)
    elif company_id:
        company = get_object_or_404(Company, pk=company_id)
        contact = CompanyContact(company=company)
        form = CompanyContactForm(instance=contact)
    else: raise Http404

    if request.method == 'POST':
        form = CompanyContactForm(request.POST, instance=contact)
        if form.is_valid():
            contact = form.save()
            return redirect(reverse('view_company', args=[contact.company.pk]))

    return render(request, 'company/contacts/edit.html', {'form': form})

def vcard(request, id):
    contact = get_object_or_404(CompanyContact, pk=id)
    person = Person()
    person.first_name = contact.first_name
    person.last_name = contact.last_name
    person.email = contact.email
    person.phone = contact.phone
    output = _vcard_string(person)
    filename = "%s%s.vcf" % (person.first_name, person.last_name)
    response = HttpResponse(output, mimetype="text/x-vCard")
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response


class Person:
    def __init__(self):
        self.first_name = ""
        self.last_name = ""
        self.email = ""
        self.phone = ""
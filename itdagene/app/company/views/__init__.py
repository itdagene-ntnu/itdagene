from django.contrib.auth.decorators import permission_required
from django.utils.translation import ugettext as _
from django.shortcuts import get_object_or_404, redirect
from itdagene.app.company.forms import BookCompanyForm, CompanyForm, ResponsibilityForm, \
    CompanyStatusForm, WaitingListCompanyForm
from itdagene.app.company.models import Company, Package
from django.forms.models import modelformset_factory
from django.urls import reverse
from django.http import Http404
from itdagene.app.feedback.models import Evaluation
from itdagene.core.models import Preference
from django.shortcuts import render
from itdagene.core.decorators import staff_required
from django.contrib.messages import add_message, SUCCESS


@staff_required()
def list_companies(request):
    if request.user.is_staff:
        user_companies = Company.objects.filter(contact=request.user).order_by(
            'status', 'name'
        ).select_related('package', 'contact').prefetch_related('company_contacts', 'contracts')
        # Put "Not intereset" last
        temp_companies = []  # Queries are lazy, use list() to execute
        not_interested_companies = []
        signed_companies = []
        for company in list(user_companies):
            if company.status == 1:
                not_interested_companies.append(company)
            elif company.status == 3:
                signed_companies.append(company)
            else:
                temp_companies.append(company)
        user_companies = temp_companies + signed_companies + not_interested_companies
    else:
        user_companies = None
    companies = Company.objects.filter(active=True).order_by('name').select_related('contact')
    return render(
        request, 'company/base.html', {
            'companies': companies,
            'user_companies': user_companies,
            'title': _('Companies')
        }
    )


@staff_required()
def view(request, id):
    company = get_object_or_404(Company.objects.select_related(), pk=id)
    evaluation, created = Evaluation.objects.get_or_create(
        company=company, preference=Preference.current_preference()
    )
    return render(
        request, 'company/view.html', {
            'company': company,
            'evaluation': evaluation,
            'title': company,
            'description': _('Company')
        }
    )


@staff_required()
def book_company(request, id):
    if request.method == 'POST':
        company = get_object_or_404(Company, pk=id)
        form = BookCompanyForm(request.POST, instance=company)
        if form.is_valid():
            Package.update_available_spots()
            company = form.save(commit=False)
            if company.package:
                if company.package.is_full:
                    company.waiting_list.add(company.package)
                    company.package = None
            company.save()
            add_message(request, SUCCESS, _('%s was booked.') % company.name)

        return redirect(company.get_absolute_url())
    else:
        raise Http404


@staff_required()
def waiting_list(request, id):
    if request.method == 'POST':
        company = get_object_or_404(Company, pk=id)
        form = WaitingListCompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            add_message(request, SUCCESS, _('Added to waiting list'))

        return redirect(company.get_absolute_url())
    else:
        raise Http404


@staff_required()
def set_status(request, id):
    if request.method == 'POST':
        company = get_object_or_404(Company, pk=id)
        form = CompanyStatusForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            add_message(request, SUCCESS, _('Status changed'))

        return redirect(company.get_absolute_url())
    else:
        raise Http404


@permission_required('company.add_company')
def add(request):
    form = CompanyForm()
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save()
            add_message(request, SUCCESS, _('Company saved.'))
            return redirect(company.get_absolute_url())
    return render(request, 'company/form.html', {'title': _('Add Company'), 'form': form})


@permission_required('company.change_company')
def edit(request, id=False):
    company = get_object_or_404(Company, pk=id)
    form = CompanyForm(instance=company)
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            company = form.save()
            add_message(request, SUCCESS, _('Comapny saved'))
            return redirect(company.get_absolute_url())
    return render(
        request, 'company/form.html',
        {
            'company': company,
            'form': form,
            'title': _('Change Company'),
            'description': company
        }
    )


@permission_required('company.change_company')
def set_responsibilities(request):
    companies = Company.objects.filter(active=True)
    form_set = modelformset_factory(Company, form=ResponsibilityForm)
    formset = form_set(queryset=companies)
    if request.method == 'POST':
        formset = form_set(request.POST, queryset=companies)
        if formset.is_valid():
            formset.save()
            add_message(request, SUCCESS, _('Changed responsibilities.'))
            return redirect(reverse('itdagene.company.list_companies'))
    return render(
        request, 'company/set_responsibilities.html', {
            'formset': formset,
            'title': _('Set Responsibilities')
        }
    )

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render_to_response, get_object_or_404, redirect
from itdagene.app.company.forms import BookCompanyForm, CompanyForm, ResponsibilityForm, ContractForm, CompanyContactForm, CompanyStatusForm
from itdagene.app.career.forms import JoblistingForm
from itdagene.app.company.models import Company, Package
from django.forms.models import modelformset_factory
from django.core.urlresolvers import reverse
from django.http import Http404
from itdagene.core.log.models import LogItem
from itdagene.app.feedback.models import EvaluationHash
from itdagene.core import Preference
from django.shortcuts import render

@login_required
def hsp(request):
    raise Http404


@permission_required('company.change_company')
def list_companies(request):
    companies = cache.get('companies')
    if request.user.profile.type == 'b':
        user_companies = cache.get('companiesforuser' + str(request.user.pk))
        if not user_companies:
            user_companies = Company.objects.filter(contact=request.user)\
            .order_by('status', 'name').select_related('package','contact', 'company_contacts','contracts')
            cache.set('companiesforuser' + str(request.user.pk), user_companies)
    else: user_companies = None
    if not companies:
        companies = Company.objects.filter(active=True).order_by('name').select_related('contact')
        cache.set('companies', companies)
    forms = [CompanyForm()]
    return render(request, 'company/base.html',
                  {'companies': companies,
                   'user_companies': user_companies,
                   'forms': forms})


@permission_required('company.change_company')
def inactive(request):
    companies = Company.objects.filter(active=False).order_by('name')
    return render(request, 'company/base.html',
                  {'companies': companies})


@permission_required('company.change_company')
def view(request, id):
    company = get_object_or_404(Company.objects.select_related(), pk=id)
    evaluation = EvaluationHash.objects.get_or_create(company=company, preference=Preference.current_preference())[0]
    forms = [ContractForm(instance=company), CompanyContactForm(instance=company), JoblistingForm(instance=company)]
    return render(request, 'company/view.html', {
        'company': company,
        'evaluation': evaluation,
        'forms': forms})


@permission_required('company.change_company')
def edit(request, id=False):
    if id:
        form_title = _(' company')
        company = get_object_or_404(Company, pk=id)
        form = CompanyForm(instance=company)
    else:
        form_title = _('Add company')
        form = CompanyForm()
        company = None
    if request.method == 'POST':
        if id:
            form = CompanyForm(request.POST, request.FILES, instance=company)
        else:
            form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save()
            request.session['message'] = {'class': 'success', 'value': _('%s was saved.') % company.name}
            return redirect(reverse('itdagene.app.company.views.list_companies'))
    return render(request, 'company/form.html',
                  {'company': company,
                   'form': form,
                   'form_title': form_title})


@permission_required('company.change_company')
def activate(request, id):
    company = get_object_or_404(Company, pk=id)
    company.active = True
    company.save()
    cache.delete('companies')
    request.session['message'] = {'class': 'success', 'value': _('%s was activated.') % company.name}
    return redirect(reverse('itdagene.app.company.views.view', args=[company.pk]))


@permission_required('company.change_company')
def deactivate(request, id):
    company = get_object_or_404(Company, pk=id)
    company.active = False
    company.save()
    cache.delete('companies')
    #add_message(request, _('%s was deactivated') % company.name, 'success')
    request.session['message'] = {'class': 'success', 'value': _('%s was deactivated.') % company.name}
    return redirect(reverse('itdagene.app.company.views.view', args=[company.pk]))


@permission_required('company.change_company')
def set_responsibilities(request):
    companies = Company.objects.filter(active=True)
    FormSet = modelformset_factory(Company, form=ResponsibilityForm)
    formset = FormSet(queryset=companies)
    if request.method == 'POST':
        formset = FormSet(request.POST,queryset=companies)
        if formset.is_valid():
            formset.save()
            for u in User.objects.filter(is_active=True):
                cache.delete('companiesforuser' + str(u.pk))
            return redirect(reverse('itdagene.app.company.views.list_companies'))
    return render(request, 'company/set_responsibilities.html',
                  {'formset': formset})


@permission_required('company.change_company')
def book_company(request, id):
    company = get_object_or_404(Company, pk=id)
    form = BookCompanyForm(instance=company)
    if request.method == 'POST':
        form = BookCompanyForm(request.POST, instance=company)
        if form.is_valid():
            Package.update_available_spots()
            company = form.save(commit=False)
            if company.package:
                if company.package.is_full:
                    company.waiting_list.add(company.package)
                    company.package = None
            company.save()
            request.session['message'] = {'class': 'success', 'value': _('%s was booked.') % company.name}
            return redirect(reverse('itdagene.app.company.views.view', args=[company.pk]))
    return render(request, 'company/form.html',
                  {'company': company,
                   'form': form})

@permission_required('company.change_company')
def waiting_list(request, id):
    company = get_object_or_404(Company, pk=id)
    form = BookCompanyForm(instance=company)
    if request.method == 'POST':
        form = BookCompanyForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            request.session['message'] = {'class': 'success', 'value': _('Added to waiting list')}
            return redirect(reverse('itdagene.app.company.views.view', args=[company.pk]))
    return render(request, 'company/form.html',
                  {'company': company,
                   'form': form})

@permission_required('company.change_company')
def set_status(request, id):
    company = get_object_or_404(Company, pk=id)
    form = CompanyStatusForm(instance=company)
    if request.method == 'POST':
        form = CompanyStatusForm(request.POST, instance=company)
        if form.is_valid():
            form.save()
            request.session['message'] = {'class': 'success', 'value': _('Status changed')}
            return redirect(reverse('itdagene.app.company.views.view', args=[company.pk]))
    return render(request, 'company/form.html',
                  {'company': company,
                   'form': form})

@permission_required('company.change_company')
def log_company(request, id):
    company = get_object_or_404(Company, pk=id)
    log = LogItem.objects.filter(content_type=ContentType.objects.get_for_model(company), object_id=company.id).reverse()
    return render(request, 'company/log.html', {'log': log, 'company': company})

@permission_required('company.change_company')
def view_contact_count(request):
    users = User.objects.filter(is_active=True, profile__type='b').select_related('companies')
    return render(request, 'company/contact_count.html',{'users':users})

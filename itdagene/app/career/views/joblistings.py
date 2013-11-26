from datetime import datetime
from itdagene.app.career.forms import JoblistingForm
from itdagene.app.company.models import Company
from itdagene.app.career.models import Joblisting
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.core.cache import cache



def view_joblisting (request, id):
    joblisting = get_object_or_404(Joblisting, pk=id)
    return render(request,'career/joblistings/view.html',
                             {'joblisting':joblisting})

def list_joblistings (request):
    if request.user.is_authenticated():
        joblistings = list(Joblisting.objects.filter(deadline__gt=datetime.now()).order_by('company','deadline'))
        joblistings += list(Joblisting.objects.filter(deadline=None).select_related('company').order_by('deadline','company'))
        return render(request, 'career/joblistings/internal_list.html',{'joblistings':joblistings})
    else:
        joblistings = cache.get('joblistings')
        if not joblistings:
            joblistings = list(Joblisting.objects.filter(company__mp=True, deadline__gt=datetime.now()).select_related('company').order_by('deadline','company'))
            joblistings += list(Joblisting.objects.filter(company__mp=True, deadline=None).select_related('company').order_by('deadline','company'))
            joblistings += list(Joblisting.objects.filter(deadline__gt=datetime.now()).exclude(company__mp=True).select_related('company').order_by('deadline','company'))
            joblistings += list(Joblisting.objects.filter(deadline=None).exclude(company__mp=True).select_related('company').order_by('deadline','company'))
            cache.set('joblistings', joblistings)

        towns = cache.get('townsinuse')
        if not towns:
            towns = []
            for j in joblistings:
                for t in j.towns.all():
                    if not t in towns: towns.append(t)
            towns.sort()
            cache.set('townsinuse', towns)

        return render(request,'career/joblistings/list.html',{'joblistings':joblistings, 'towns': towns})

@permission_required('career.change_joblisting')
def edit(request, id=None, company_id=None):
    if id:
        joblisting = get_object_or_404(Joblisting, pk=id)
    else:
        company = get_object_or_404(Company, pk=company_id)
        joblisting = Joblisting(company=company)
    form = JoblistingForm(instance=joblisting)
    if request.method == 'POST':
        form = JoblistingForm(request.POST, request.FILES, instance=joblisting)
        if form.is_valid():
            form.save()
            return redirect(reverse('itdagene.app.career.views.joblistings.view_joblisting', args=[joblisting.pk]))
    return render(request, 'career/joblistings/edit.html',
                 {'joblisting':joblisting,
                  'form': form})


@permission_required('career.change_joblisting')
def deactivate(request, id):
    joblisting = get_object_or_404(Joblisting, pk=id)
    joblisting.deadline = datetime(2010,8,17)
    joblisting.save()
    return redirect(reverse('joblistings'))
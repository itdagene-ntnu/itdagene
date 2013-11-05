from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect
from itdagene.app.company.models import Package
from itdagene.app.company.forms import PackageForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render


@permission_required('company.change_package')
def list(request):
    packages = Package.objects.all()
    return render(request, 'company/packages/base.html',
                  {'packages': packages})


@permission_required('company.change_package')
def view(request, id):
    package = get_object_or_404(Package, pk=id)
    return render(request, 'company/packages/view.html',
                  {'package': package})

@permission_required('company.change_package')
def edit(request, id=False):

    if id:
        form_title = _('Edit package')
        package = get_object_or_404(Package, pk=id)
        form = PackageForm(instance=package)
    else:
        form_title = _('Add package')
        package = None
        form = PackageForm()
    if request.method == 'POST':
        if id:
            form = PackageForm(request.POST, instance=package)
        else:
            form = PackageForm(request.POST)
        if form.is_valid():
            package = form.save()
            redirect(reverse('itdagene.app.company.views.packages.view', args=[package.pk]))
    return render(request, 'company/packages/form.html',
                             {'package': package,
                              'form': form,
                              'form_title': form_title})
from django.contrib.auth.decorators import permission_required
from django.contrib.messages import SUCCESS, add_message
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from itdagene.app.company.forms import PackageForm
from itdagene.app.company.models import Package
from itdagene.core.decorators import staff_required


@staff_required()
def list(request):
    packages = Package.objects.all()
    return render(
        request, 'company/packages/base.html', {
            'packages': packages,
            'title': _('Packages')
        }
    )


@staff_required()
def view(request, id):
    package = get_object_or_404(Package, pk=id)
    return render(
        request, 'company/packages/view.html',
        {
            'package': package,
            'title': _('Package'),
            'description': package
        }
    )


@permission_required('company.change_package')
def add(request):
    form = PackageForm()
    if request.method == 'POST':
        form = PackageForm(request.POST)
        if form.is_valid():
            form.save()
            add_message(request, SUCCESS, _('Package added.'))
            return redirect(reverse('itdagene.company.packages.list'))
    return render(request, 'company/form.html', {'form': form, 'title': _('Add Package')})


@permission_required('company.change_package')
def edit(request, id):
    package = get_object_or_404(Package, pk=id)
    form = PackageForm(instance=package)

    if request.method == 'POST':
        form = PackageForm(request.POST, instance=package)
        if form.is_valid():
            form.save()
            add_message(request, SUCCESS, _('Package saved.'))
            return redirect(reverse('itdagene.company.packages.list'))
    return render(
        request, 'company/form.html',
        {
            'package': package,
            'form': form,
            'title': _('Edit Package'),
            'description': package
        }
    )

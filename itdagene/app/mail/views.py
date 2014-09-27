from django.shortcuts import redirect, render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import permission_required
from itdagene.app.mail.forms import MailMappingForm
from itdagene.app.mail.models import MailMapping
from django.core.urlresolvers import reverse


@permission_required('mail.add_mailmapping')
def add_mailmapping(request):
    if request.method == 'POST':
        form = MailMappingForm(request.POST, request.FILES)
        if form.is_valid():
            mapping = form.save()
            if request.user.has_perm('mail.change_mailmapping'):
                return redirect(reverse('app.mail.views.view_mailmapping', args=[mapping.pk]))
            else:
                return redirect(reverse('app.mail.views.add_mailmapping'))
    else:
        form = MailMappingForm()
    return render(request, 'mail/add_mailmapping.html', {'form': form, 'title':_('Add Mail Mapping')})


@permission_required('mail.change_mailmapping')
def list_mailmapping(request):
    mappings = MailMapping.objects.all().order_by('address')
    return render(request, 'mail/list_mailmapping.html', {'mappings':mappings, 'title': _('Mail mappings')})


@permission_required('mail.change_mailmapping')
def change_mailmapping(request, pk):
    mapping = get_object_or_404(MailMapping, pk=pk)
    if request.method == 'POST':
        form = MailMappingForm(request.POST, request.FILES, instance=mapping)
        if form.is_valid():
            form.save()
            return redirect(reverse('app.mail.views.view_mailmapping', args=[mapping.pk]))
    else:
        form = MailMappingForm(instance=mapping)
    return render(request, 'mail/change_mailmapping.html', {'mapping': mapping, 'form': form, 'title':_('Change Mail Mapping'), 'description': mapping})


@permission_required('mail.change_mailmapping')
def view_mailmapping(request, pk):
    mapping = get_object_or_404(MailMapping, pk=pk)
    return render(request, 'mail/view_mailmapping.html', {'mapping':mapping, 'title': _('Mail Mapping'), 'description': mapping})


@permission_required('mail.delete_mailmapping')
def delete_mailmapping(request, pk):
    mapping = get_object_or_404(MailMapping, pk=pk)

    if request.method == 'POST':
        mapping.delete()
        return redirect(reverse('app.mail.views.list_mailmapping'))

    return render(request, 'mail/delete_mailmapping.html', {'mapping': mapping, 'title': _('Delete Mail Mapping'), 'description': mapping})


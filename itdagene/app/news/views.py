from django.shortcuts import redirect, get_object_or_404
from itdagene.app.news.forms import AnnouncementForm
from itdagene.app.news.models import Announcement
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from itdagene.core.decorators import staff_or_404

def view_announcement(request, id):
    announcement = get_object_or_404(Announcement, pk=id)
    return render(request,'news/view.html',{'announcement': announcement})


@permission_required('news.add_announcement')
def create_announcement(request):
    form = AnnouncementForm()
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            announcement = form.save()
            return redirect(reverse('itdagene.app.news.views.view_announcement', args=[announcement.pk]))
    return render(request, 'news/edit.html', {'form': form, 'title': _('Add Announcement')})

@permission_required('news.change_announcement')
def edit_announcement(request, id=False):
    if id:
        ann = get_object_or_404(Announcement, pk=id)
        form = AnnouncementForm(instance=ann)
        if request.method == 'POST':
            form = AnnouncementForm(request.POST, request.FILES, instance=ann)
    else:
        form = AnnouncementForm()
        if request.method == 'POST':
            form = AnnouncementForm(request.POST, request.FILES)
    if request.method == 'POST' and form.is_valid():
        instance = form.save()
        return redirect(reverse('itdagene.app.news.views.view_announcement', args=[instance.pk]))
    return render(request,'news/edit.html',{'form': form, 'title': _('Edit Announcement')})


@staff_or_404
def admin(request):
    announcements =  Announcement.objects.order_by('id').reverse()
    return render(request, 'news/admin.html', {'announcements': announcements, 'title': _('Announcement Admin')})
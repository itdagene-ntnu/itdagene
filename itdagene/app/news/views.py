from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.cache import cache_page
from itdagene.app.news.forms import AnnouncementForm
from itdagene.app.news.models import Announcement
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.core.urlresolvers import reverse


def view_announcement(request, id):
    announcement = get_object_or_404(Announcement, pk=id)
    return render(request,'news/view.html',{'announcement': announcement})


@permission_required('news.change_announcement')
def create_announcement(request):
    return edit_announcement(request)


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
    return render(request,'news/edit.html',{'form': form})
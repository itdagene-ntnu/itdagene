from django.contrib.auth.decorators import permission_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from itdagene.app.news.forms import AnnouncementForm
from itdagene.app.news.models import Announcement
from itdagene.core.decorators import staff_required


@permission_required("news.add_announcement")
def create_announcement(request: HttpRequest) -> HttpResponse:
    form = AnnouncementForm()
    if request.method == "POST":
        form = AnnouncementForm(request.POST, request.FILES)
        if form.is_valid():
            announcement = form.save()
            return redirect(
                reverse("itdagene.news.edit_announcement", args=[announcement.pk])
            )
    return render(
        request,
        "news/edit.html",
        {"form": form, "title": _("Add Announcement")},
    )


@permission_required("news.change_announcement")
def edit_announcement(request: HttpRequest, id_: bool = False) -> HttpResponse:
    if id_:
        ann = get_object_or_404(Announcement, pk=id_)
        form = AnnouncementForm(instance=ann)
        if request.method == "POST":
            form = AnnouncementForm(request.POST, request.FILES, instance=ann)
    else:
        form = AnnouncementForm()
        if request.method == "POST":
            form = AnnouncementForm(request.POST, request.FILES)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect(reverse("itdagene.news.admin"))
    return render(
        request,
        "news/edit.html",
        {"form": form, "title": _("Edit Announcement")},
    )


@staff_required()
def admin(request: HttpRequest) -> HttpResponse:
    announcements = Announcement.objects.order_by("id").reverse()
    return render(
        request,
        "news/admin.html",
        {"announcements": announcements, "title": _("Announcement Admin")},
    )

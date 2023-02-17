from django.contrib.auth.decorators import permission_required
from django.contrib.messages import SUCCESS, add_message
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from itdagene.app.career.forms import JoblistingForm, JoblistingTownForm
from itdagene.app.career.models import Joblisting
from itdagene.core.decorators import staff_required


@staff_required()
def list(request):
    joblistings = Joblisting.objects.filter(
        (Q(deadline__gte=timezone.now()) | Q(deadline__isnull=True)), is_active=True
    )

    return render(
        request,
        "career/list.html",
        {"joblistings": joblistings, "title": _("Joblistings")},
    )


@permission_required("career.add_joblisting")
def add(request):
    form = JoblistingForm()
    if request.method == "POST":
        form = JoblistingForm(request.POST, request.FILES)
        if form.is_valid():
            joblisting = form.save()
            add_message(request, SUCCESS, _("Joblisting saved."))
            return redirect(reverse("itdagene.career.view", args=[joblisting.pk]))
    return render(
        request, "career/form.html", {"title": _("Add Joblisting"), "form": form}
    )


@staff_required()
def view(request, pk):
    joblisting = get_object_or_404(Joblisting, pk=pk)
    return render(
        request,
        "career/view.html",
        {
            "joblisting": joblisting,
            "title": _("Joblisting"),
            "description": str(joblisting),
        },
    )


@permission_required("career.change_joblisting")
def edit(request, pk):
    joblisting = get_object_or_404(Joblisting, pk=pk)
    form = JoblistingForm(instance=joblisting)

    if request.method == "POST":
        form = JoblistingForm(request.POST, request.FILES, instance=joblisting)
        if form.is_valid():
            form.save()
            add_message(request, SUCCESS, _("Joblisting saved."))
            return redirect(reverse("itdagene.career.view", args=[joblisting.pk]))
    return render(
        request,
        "career/form.html",
        {
            "title": _("Edit Joblisting"),
            "form": form,
            "description": str(joblisting),
            "joblisting": joblisting,
        },
    )


@permission_required("career.delete_joblisting")
def delete(request, pk):
    joblisting = get_object_or_404(Joblisting, pk=pk)
    if request.method == "POST":
        joblisting.is_active = False
        joblisting.save()
        add_message(request, SUCCESS, _("Joblisting deleted."))
        return redirect(reverse("itdagene.career.list"))

    return render(
        request,
        "career/delete.html",
        {
            "joblisting": joblisting,
            "title": _("Delete Joblisting"),
            "description": str(joblisting),
        },
    )


@permission_required("career.add_town")
def add_town(request):
    form = JoblistingTownForm()
    if request.method == "POST":
        form = JoblistingTownForm(request.POST)
        if form.is_valid():
            form.save()
            add_message(request, SUCCESS, _("Town added."))
            return redirect(reverse("itdagene.career.list"))
    return render(request, "career/form.html", {"form": form, "title": _("Add Town")})

from django.contrib.auth.decorators import permission_required
from django.contrib.messages import SUCCESS, add_message
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from itdagene.app.events.models import Event
from itdagene.app.stands.forms import DigitalStandForm
from itdagene.app.stands.models import DigitalStand
from itdagene.core.decorators import staff_required


@staff_required()
def list(request):
    stands = DigitalStand.objects.all()

    return render(
        request, "stands/list.html", {"stands": stands, "title": _("Stands")},
    )


@permission_required("stands.add_stand")
def add(request):
    form = DigitalStandForm()
    if request.method == "POST":
        form = DigitalStandForm(request.POST)
        if form.is_valid():
            stand = form.save()
            add_message(request, SUCCESS, _("Stand saved."))
            return redirect(reverse("itdagene.stands.view", args=[stand.pk]))
    return render(request, "stands/form.html", {"title": _("Add stand"), "form": form})


@staff_required()
def view(request, pk):
    stand = get_object_or_404(DigitalStand, pk=pk)
    stand_events = Event.objects.filter(stand=stand)
    return render(
        request,
        "stands/view.html",
        {
            "stand": stand,
            "stand_events": stand_events,
            "title": _("Stand"),
            "description": str(stand),
        },
    )


@permission_required("stands.change_stand")
def edit(request, pk):
    stand = get_object_or_404(DigitalStand, pk=pk)
    form = DigitalStandForm(instance=stand)

    if request.method == "POST":
        form = DigitalStandForm(request.POST, request.FILES, instance=stand)
        if form.is_valid():
            form.save()
            add_message(request, SUCCESS, _("stand saved."))
            return redirect(reverse("itdagene.stands.view", args=[stand.pk]))
    return render(
        request,
        "stands/form.html",
        {
            "title": _("Edit stand"),
            "form": form,
            "description": str(stand),
            "stand": stand,
        },
    )


@permission_required("stands.delete_stand")
def delete(request, pk):
    stand = get_object_or_404(DigitalStand, pk=pk)
    if request.method == "POST":
        stand.delete()
        add_message(request, SUCCESS, _("stand deleted."))
        return redirect(reverse("itdagene.stands.list"))

    return render(
        request,
        "stands/delete.html",
        {"stand": stand, "title": _("Delete stand"), "description": str(stand)},
    )

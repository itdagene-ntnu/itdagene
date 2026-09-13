import hashlib
import mimetypes
from typing import Any

from django.contrib.auth.decorators import permission_required
from django.contrib.messages import SUCCESS, add_message
from django.http import FileResponse, HttpRequest, HttpResponse, HttpResponseNotModified
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from itdagene.app.events.models import Event
from itdagene.app.stands.forms import DigitalStandForm
from itdagene.app.stands.models import DigitalStand, StandMap, StandMapRelease
from itdagene.core.decorators import staff_required
from itdagene.core.models import Preference


def published_map_background(request: HttpRequest, pk: Any) -> HttpResponse:
    stand_map = get_object_or_404(
        StandMap,
        pk=pk,
        release__preference=Preference.current_preference(),
        release__preference__stands_published=True,
        release__status=StandMapRelease.PUBLISHED,
    )

    # Published maps are immutable and a new release gets new rows, so the bytes
    # behind one URL never change. "no-cache" still forces a revalidation on
    # every use, which keeps unpublishing immediate: the next request runs the
    # lookup above and 404s. What it avoids is re-sending a megabyte of PNG on
    # every page view and every day switch.
    etag = '"{}"'.format(
        hashlib.sha1(
            "{}:{}".format(stand_map.pk, stand_map.background.name).encode("utf-8")
        ).hexdigest()
    )

    if request.META.get("HTTP_IF_NONE_MATCH") == etag:
        response: HttpResponse = HttpResponseNotModified()
    else:
        content_type = (
            mimetypes.guess_type(stand_map.background.name)[0]
            or "application/octet-stream"
        )
        response = FileResponse(
            stand_map.background.open("rb"), content_type=content_type
        )

    response["ETag"] = etag
    response["Cache-Control"] = "no-cache, private"
    return response


@staff_required()
def list(request: HttpRequest) -> HttpResponse:
    stands = DigitalStand.objects.all()

    return render(
        request,
        "stands/list.html",
        {"stands": stands, "title": _("Stander")},
    )


@permission_required("stands.add_stand")
def add(request: HttpRequest) -> HttpResponse:
    form = DigitalStandForm()
    if request.method == "POST":
        form = DigitalStandForm(request.POST)
        if form.is_valid():
            stand = form.save()
            add_message(request, SUCCESS, _("Standen er lagret."))
            return redirect(reverse("itdagene.stands.view", args=[stand.pk]))
    return render(
        request,
        "stands/form.html",
        {"title": _("Legg til stand"), "form": form},
    )


@staff_required()
def view(request: HttpRequest, pk: Any) -> HttpResponse:
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
def edit(request: HttpRequest, pk: Any) -> HttpResponse:
    stand = get_object_or_404(DigitalStand, pk=pk)
    form = DigitalStandForm(instance=stand)

    if request.method == "POST":
        form = DigitalStandForm(request.POST, request.FILES, instance=stand)
        if form.is_valid():
            form.save()
            add_message(request, SUCCESS, _("Standen er lagret."))
            return redirect(reverse("itdagene.stands.view", args=[stand.pk]))
    return render(
        request,
        "stands/form.html",
        {
            "title": _("Rediger stand"),
            "form": form,
            "description": str(stand),
            "stand": stand,
        },
    )


@permission_required("stands.delete_stand")
def delete(request: HttpRequest, pk: Any) -> HttpResponse:
    stand = get_object_or_404(DigitalStand, pk=pk)
    if request.method == "POST":
        stand.delete()
        add_message(request, SUCCESS, _("Standen er slettet."))
        return redirect(reverse("itdagene.stands.list"))

    return render(
        request,
        "stands/delete.html",
        {
            "stand": stand,
            "title": _("Slett stand"),
            "description": str(stand),
        },
    )

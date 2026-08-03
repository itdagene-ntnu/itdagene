from typing import Any

from django.contrib.auth.decorators import permission_required
from django.contrib.messages import ERROR, SUCCESS, add_message
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.dateparse import parse_date
from django.utils.translation import gettext_lazy as _

from itdagene.app.stands.forms import StandMapForm, StandPlacementForm
from itdagene.app.stands.models import StandMap, StandMapRelease, StandPlacement
from itdagene.core.models import Preference


def _placement_form_prefix(placement_id: Any) -> str:
    return "placement-{}".format(placement_id)


def _new_placement_form_prefix(stand_map_id: Any) -> str:
    return "new-placement-{}".format(stand_map_id)


def _release_or_404(pk: Any) -> StandMapRelease:
    return get_object_or_404(
        StandMapRelease,
        pk=pk,
        preference=Preference.current_preference(),
    )


def _release_edit_url(pk: Any, stand_map_id: Any = None) -> str:
    url = reverse("itdagene.stand_maps.edit", args=[pk])
    if stand_map_id is not None:
        return "{}#stand-map-{}".format(url, stand_map_id)
    return url


def _published_release(preference: Preference):
    return (
        StandMapRelease.objects.filter(
            preference=preference,
            status=StandMapRelease.PUBLISHED,
        )
        .order_by("-revision")
        .first()
    )


def _lock_draft(release_id: Any, expected_lock_version: Any) -> StandMapRelease:
    release = StandMapRelease.objects.select_for_update().get(pk=release_id)
    if release.status != StandMapRelease.DRAFT:
        raise ValidationError(_("Bare kladder kan redigeres."))
    if release.lock_version != int(expected_lock_version):
        raise ValidationError(_("Kladden er endret. Last siden på nytt før du lagrer."))
    release.lock_version += 1
    release.save(update_fields=("lock_version", "updated_at"))
    return release


@permission_required("stands.view_standmaprelease")
def release_list(request: HttpRequest) -> HttpResponse:
    preference = Preference.current_preference()
    releases = StandMapRelease.objects.filter(preference=preference).select_related(
        "published_by"
    )
    return render(
        request,
        "stands/maps/list.html",
        {
            "preference": preference,
            "public_release": _published_release(preference),
            "releases": releases,
            "title": _("Standkart"),
        },
    )


@permission_required("stands.add_standmaprelease")
def release_create(request: HttpRequest) -> HttpResponse:
    preference = Preference.current_preference()
    if request.method == "POST":
        with transaction.atomic():
            preference = Preference.objects.select_for_update().get(pk=preference.pk)
            revision = (
                StandMapRelease.objects.filter(preference=preference)
                .order_by("-revision")
                .values_list("revision", flat=True)
                .first()
                or 0
            ) + 1
            release = StandMapRelease.objects.create(
                preference=preference, revision=revision
            )
            source = (
                StandMapRelease.objects.filter(
                    preference=preference,
                    status=StandMapRelease.PUBLISHED,
                )
                .prefetch_related("maps__placements")
                .order_by("-revision")
                .first()
            )
            if source:
                for source_map in source.maps.all():
                    stand_map = StandMap.objects.create(
                        release=release,
                        date=source_map.date,
                        label=source_map.label,
                        location=source_map.location,
                        background=source_map.background.name,
                    )
                    StandPlacement.objects.bulk_create(
                        [
                            StandPlacement(
                                stand_map=stand_map,
                                company=placement.company,
                                stand_number=placement.stand_number,
                                x_percent=placement.x_percent,
                                y_percent=placement.y_percent,
                                company_name=placement.company_name,
                                company_slug=placement.company_slug,
                            )
                            for placement in source_map.placements.all()
                        ]
                    )
        add_message(request, SUCCESS, _("Kladden for standkartet er opprettet."))
        return redirect("itdagene.stand_maps.edit", pk=release.pk)
    return render(
        request,
        "stands/maps/create.html",
        {"title": _("Opprett kladd for standkart"), "preference": preference},
    )


@permission_required("stands.change_standmaprelease")
def release_edit(request: HttpRequest, pk: Any) -> HttpResponse:
    release = _release_or_404(pk)
    if request.method == "POST":
        return_to_map = None
        action = request.POST.get("action")
        try:
            with transaction.atomic():
                release = _lock_draft(pk, request.POST.get("lock_version"))
                if action == "save-map":
                    stand_map = StandMap(release=release)
                    map_id = request.POST.get("map_id")
                    if map_id:
                        stand_map = get_object_or_404(
                            StandMap, pk=map_id, release=release
                        )
                    else:
                        try:
                            submitted_date = parse_date(request.POST.get("date", ""))
                        except ValueError:
                            submitted_date = None
                        if submitted_date:
                            stand_map = (
                                release.maps.select_for_update()
                                .filter(date=submitted_date)
                                .first()
                                or stand_map
                            )
                    form = StandMapForm(request.POST, request.FILES, instance=stand_map)
                    if form.is_valid():
                        form.save()
                        add_message(request, SUCCESS, _("Kartet er lagret."))
                    else:
                        raise ValidationError(form.errors.as_text())
                elif action == "delete-map":
                    get_object_or_404(
                        StandMap, pk=request.POST.get("map_id"), release=release
                    ).delete()
                    add_message(request, SUCCESS, _("Kartet er fjernet."))
                elif action == "save-placement":
                    stand_map = get_object_or_404(
                        StandMap, pk=request.POST.get("map_id"), release=release
                    )
                    return_to_map = stand_map.pk
                    placement = StandPlacement(stand_map=stand_map)
                    placement_id = request.POST.get("placement_id")
                    if placement_id:
                        placement = get_object_or_404(
                            StandPlacement, pk=placement_id, stand_map=stand_map
                        )
                        prefix = _placement_form_prefix(placement.pk)
                    else:
                        prefix = _new_placement_form_prefix(stand_map.pk)
                    form = StandPlacementForm(
                        request.POST,
                        instance=placement,
                        prefix=prefix,
                    )
                    if form.is_valid():
                        form.save()
                        add_message(request, SUCCESS, _("Plasseringen er lagret."))
                    else:
                        raise ValidationError(form.errors.as_text())
                elif action == "delete-placement":
                    StandPlacement.objects.filter(
                        pk=request.POST.get("placement_id"),
                        stand_map__release=release,
                    ).delete()
                    add_message(request, SUCCESS, _("Plasseringen er fjernet."))
                else:
                    raise ValidationError(_("Ukjent handling i standkartet."))
        except (ValidationError, TypeError, ValueError) as error:
            add_message(request, ERROR, str(error))
        except IntegrityError:
            if action == "save-map":
                message = _(
                    "Kartet kunne ikke lagres fordi det allerede finnes et kart "
                    "for denne dagen. Last siden på nytt og prøv igjen."
                )
            elif action == "save-placement":
                message = _(
                    "Plasseringen kunne ikke lagres fordi bedriften eller "
                    "standnummeret allerede er brukt på dette kartet."
                )
            else:
                raise
            add_message(request, ERROR, message)
        return redirect(_release_edit_url(pk, return_to_map))
    maps = release.maps.prefetch_related("placements__company").all()
    editor_maps = []
    for stand_map in maps:
        editor_maps.append(
            {
                "stand_map": stand_map,
                "map_form": StandMapForm(instance=stand_map),
                "placement_forms": [
                    (
                        placement,
                        StandPlacementForm(
                            instance=placement,
                            prefix=_placement_form_prefix(placement.pk),
                        ),
                    )
                    for placement in stand_map.placements.all()
                ],
                "new_placement_form": StandPlacementForm(
                    prefix=_new_placement_form_prefix(stand_map.pk),
                    initial={
                        "stand_number": StandPlacement.next_available_number(stand_map)
                    },
                ),
            }
        )
    return render(
        request,
        "stands/maps/edit.html",
        {
            "release": release,
            "public_release": _published_release(release.preference),
            "editor_maps": editor_maps,
            "new_map_form": StandMapForm(),
            "title": _("Rediger kladd for standkart")
            if release.status == StandMapRelease.DRAFT
            else _("Vis standkart"),
        },
    )


@permission_required("stands.publish_standmaprelease")
def release_publish(request: HttpRequest, pk: Any) -> HttpResponse:
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    release = _release_or_404(pk)
    try:
        published_release = StandMapRelease.publish(
            release.pk,
            int(request.POST.get("lock_version")),
            request.user,
        )
        if published_release.preference.stands_published:
            message = _("Standkartversjonen er publisert og vises på nettsiden.")
        else:
            message = _(
                "Standkartversjonen er publisert. Vis stands er fortsatt slått av, "
                "så nettsiden viser plassholderen."
            )
        add_message(request, SUCCESS, message)
    except (ValidationError, TypeError, ValueError) as error:
        add_message(request, ERROR, str(error))
    return redirect("itdagene.stand_maps.edit", pk=pk)

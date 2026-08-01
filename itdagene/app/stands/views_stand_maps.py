from typing import Any

from django.contrib.auth.decorators import permission_required
from django.contrib.messages import ERROR, SUCCESS, add_message
from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _

from itdagene.app.stands.forms import StandMapForm, StandPlacementForm
from itdagene.app.stands.models import StandMap, StandMapRelease, StandPlacement
from itdagene.core.models import Preference


def _release_or_404(pk: Any) -> StandMapRelease:
    return get_object_or_404(
        StandMapRelease,
        pk=pk,
        preference=Preference.current_preference(),
    )


def _lock_draft(release_id: Any, expected_lock_version: Any) -> StandMapRelease:
    release = StandMapRelease.objects.select_for_update().get(pk=release_id)
    if release.status != StandMapRelease.DRAFT:
        raise ValidationError(_("Only draft releases can be edited."))
    if release.lock_version != int(expected_lock_version):
        raise ValidationError(_("This draft changed. Reload it before saving."))
    release.lock_version += 1
    release.save(update_fields=("lock_version", "updated_at"))
    return release


@permission_required("stands.view_standmaprelease")
def release_list(request: HttpRequest) -> HttpResponse:
    releases = StandMapRelease.objects.filter(
        preference=Preference.current_preference()
    ).select_related("published_by")
    return render(
        request,
        "stands/maps/list.html",
        {"releases": releases, "title": _("Stand maps")},
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
        add_message(request, SUCCESS, _("Stand map draft created."))
        return redirect("itdagene.stand_maps.edit", pk=release.pk)
    return render(
        request,
        "stands/maps/create.html",
        {"title": _("Create stand map draft"), "preference": preference},
    )


@permission_required("stands.change_standmaprelease")
def release_edit(request: HttpRequest, pk: Any) -> HttpResponse:
    release = _release_or_404(pk)
    if request.method == "POST":
        try:
            with transaction.atomic():
                release = _lock_draft(pk, request.POST.get("lock_version"))
                action = request.POST.get("action")
                if action == "save-map":
                    stand_map = StandMap(release=release)
                    map_id = request.POST.get("map_id")
                    if map_id:
                        stand_map = get_object_or_404(
                            StandMap, pk=map_id, release=release
                        )
                    form = StandMapForm(request.POST, request.FILES, instance=stand_map)
                    if form.is_valid():
                        form.save()
                        add_message(request, SUCCESS, _("Map saved."))
                    else:
                        raise ValidationError(form.errors.as_text())
                elif action == "delete-map":
                    get_object_or_404(
                        StandMap, pk=request.POST.get("map_id"), release=release
                    ).delete()
                    add_message(request, SUCCESS, _("Map removed."))
                elif action == "save-placement":
                    stand_map = get_object_or_404(
                        StandMap, pk=request.POST.get("map_id"), release=release
                    )
                    placement = StandPlacement(stand_map=stand_map)
                    placement_id = request.POST.get("placement_id")
                    if placement_id:
                        placement = get_object_or_404(
                            StandPlacement, pk=placement_id, stand_map=stand_map
                        )
                    form = StandPlacementForm(request.POST, instance=placement)
                    if form.is_valid():
                        form.save()
                        add_message(request, SUCCESS, _("Placement saved."))
                    else:
                        raise ValidationError(form.errors.as_text())
                elif action == "delete-placement":
                    StandPlacement.objects.filter(
                        pk=request.POST.get("placement_id"),
                        stand_map__release=release,
                    ).delete()
                    add_message(request, SUCCESS, _("Placement removed."))
                else:
                    raise ValidationError(_("Unknown editor action."))
        except (ValidationError, TypeError, ValueError) as error:
            add_message(request, ERROR, str(error))
        return redirect("itdagene.stand_maps.edit", pk=pk)
    maps = release.maps.prefetch_related("placements__company").all()
    editor_maps = []
    for stand_map in maps:
        editor_maps.append(
            {
                "stand_map": stand_map,
                "map_form": StandMapForm(instance=stand_map),
                "placement_forms": [
                    (placement, StandPlacementForm(instance=placement))
                    for placement in stand_map.placements.all()
                ],
                "new_placement_form": StandPlacementForm(),
            }
        )
    return render(
        request,
        "stands/maps/edit.html",
        {
            "release": release,
            "editor_maps": editor_maps,
            "new_map_form": StandMapForm(),
            "title": _("Edit stand map draft"),
        },
    )


@permission_required("stands.publish_standmaprelease")
def release_publish(request: HttpRequest, pk: Any) -> HttpResponse:
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    release = _release_or_404(pk)
    try:
        StandMapRelease.publish(
            release.pk,
            int(request.POST.get("lock_version")),
            request.user,
        )
        add_message(request, SUCCESS, _("Stand map published."))
    except (ValidationError, TypeError, ValueError) as error:
        add_message(request, ERROR, str(error))
    return redirect("itdagene.stand_maps.edit", pk=pk)

from typing import Any

from django.contrib.auth.decorators import permission_required
from django.contrib.messages import SUCCESS, add_message
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from itdagene.app.gallery.forms import PhotoForm
from itdagene.app.gallery.models import Photo


def list_photos(request: HttpRequest) -> HttpResponse:
    photos = Photo.objects.all().order_by("order")
    return render(
        request,
        "gallery/base.html",
        {"photos": photos, "title": _("All Photos")},
    )


@permission_required("gallery.add_photo")
def add_photo(request: HttpRequest) -> HttpResponse:
    form = PhotoForm()
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            add_message(request, SUCCESS, _("Photo added."))
            return redirect(reverse("itdagene.gallery.list_photos"))
    return render(request, "gallery/form.html", {"form": form, "title": _("Add Photo")})


@permission_required("gallery.edit_photo")
def edit_photo(request: HttpRequest, pk: Any) -> HttpResponse:
    photo = get_object_or_404(Photo, pk=pk)
    form = PhotoForm(instance=photo)
    if request.method == "POST":
        form = PhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            photo = form.save()
            add_message(request, SUCCESS, _("Photo saved."))
            return redirect(reverse("itdagene.gallery.list_photos"))
    return render(
        request,
        "gallery/form.html",
        {
            "photo": photo,
            "form": form,
            "title": _("Edit Photo"),
        },
    )


@permission_required("gallery.delete_photo")
def delete_photo(request: HttpRequest, pk: Any) -> HttpResponse:
    photo = get_object_or_404(Photo, pk=pk)
    if request.method == "POST":
        photo.delete()
        add_message(request, SUCCESS, _("Photo deleted."))
        return redirect(reverse("itdagene.gallery.list_photos"))
    return render(
        request,
        "gallery/delete.html",
        {
            "photo": photo,
            "title": _("Delete Photo"),
            "description": str(photo),
        },
    )


@permission_required("gallery.edit_photo")
def reorder_photos(request: HttpRequest) -> HttpResponse:
    photos = Photo.objects.all().order_by("order")

    if request.method == "POST":
        photo_orders = request.POST.getlist("photo_order")

        # Midlertidig fase: unngå unique conflict ved å bruke midlertidige verdier
        temp_mapping = {}
        for i, order_value in enumerate(photo_orders, start=1):
            photo = Photo.objects.get(id=order_value)
            photo.order = i * 100  # midlertidig unik verdi
            photo.save()
            temp_mapping[order_value] = photo  # lagre referansen

        # Endelig rekkefølge
        for i, order_value in enumerate(photo_orders, start=1):
            photo = temp_mapping[order_value]
            photo.order = i
            photo.save()

        add_message(request, SUCCESS, _("Photo order updated."))
        return redirect(reverse("itdagene.gallery.list_photos"))

    return render(
        request,
        "gallery/reorder_photos.html",
        {
            "photos": photos,
            "title": _("Update Photo Order"),
        },
    )

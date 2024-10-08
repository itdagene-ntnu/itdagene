from typing import Any

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.contrib.messages import SUCCESS, add_message
from django.db.models import Q
from django.http import Http404, HttpRequest
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from itdagene.app.mail.senders import users_send_welcome_email
from itdagene.app.users import vcard_string
from itdagene.app.users.forms import SimpleUserEditForm, UserCreateForm, UserEditForm
from itdagene.core.log.models import LogItem
from itdagene.core.models import Preference, User


@login_required
def user_list(request: HttpRequest) -> HttpResponse:
    if not request.user.is_staff:
        persons = User.objects.filter(Q(is_staff=True) | Q(id=request.user.id)).filter(
            is_active=True, year=request.user.year
        )
    else:
        persons = User.objects.filter(is_active=True)

    persons = persons.order_by("-year", "username")
    return render(
        request,
        "users/list.html",
        {"persons": persons, "title": _("User Admin")},
    )


@login_required
def user_detail(request: HttpRequest, pk: Any) -> HttpResponse:
    try:
        if not request.user.is_staff:
            person = (
                User.objects.filter(Q(is_staff=True) | Q(id=request.user.id))
                .filter(is_active=True, year=request.user.year)
                .get(pk=pk)
            )
        else:
            person = User.objects.filter(is_active=True).order_by("username").get(pk=pk)
    except Exception:
        raise Http404
    current_year = Preference.current_preference().year
    return render(
        request,
        "users/detail.html",
        {
            "person": person,
            "current_year": current_year,
            "title": _("User Detail"),
            "description": person.get_full_name(),
        },
    )


@permission_required("core.delete_user")
def user_delete(request: HttpRequest, pk: Any) -> HttpResponse:
    person = get_object_or_404(User, pk=pk, is_active=True)

    if request.method == "POST":
        person.is_active = False
        person.save()
        return redirect(reverse("itdagene.users.user_list"))

    return render(
        request,
        "users/delete.html",
        {
            "person": person,
            "title": _("Delete User"),
            "description": person.get_full_name(),
        },
    )


@login_required
def user_edit(request: HttpRequest, pk: Any) -> HttpResponse:
    if not request.user.has_perm("core.change_user") and not request.user.pk == int(pk):
        return redirect(reverse("itdagene.users.user_list"))

    person = get_object_or_404(User, pk=pk, is_active=True)

    if request.method == "POST":
        if request.user.is_superuser:
            form = UserEditForm(request.POST, request.FILES, instance=person)
        else:
            form = SimpleUserEditForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            person = form.save()
            LogItem.log_it(person, "EDIT", 2)
            return redirect(reverse("itdagene.users.user_detail", args=[person.pk]))
    elif request.user.is_superuser:
        form = UserEditForm(instance=person)
    else:
        form = SimpleUserEditForm(instance=person)

    return render(
        request,
        "users/edit.html",
        {
            "form": form,
            "person": person,
            "title": _("Edit User"),
            "description": person.get_full_name(),
        },
    )


@login_required
def user_edit_password(request: HttpRequest, pk: Any) -> HttpResponse:
    if not request.user.has_perm("core.change_user") and not request.user.pk == int(pk):
        return redirect(reverse("itdagene.users.user_list"))

    person = get_object_or_404(User, pk=pk, is_active=True)

    if request.method == "POST":
        if request.user.is_superuser:
            form = SetPasswordForm(user=person, data=request.POST)
        else:
            form = PasswordChangeForm(user=person, data=request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse("itdagene.users.user_detail", args=[person.pk]))

    elif request.user.is_superuser:
        form = SetPasswordForm(person)
    else:
        form = PasswordChangeForm(person)

    return render(
        request,
        "users/edit_password.html",
        {
            "person": person,
            "form": form,
            "title": _("Change Password"),
            "description": person.get_full_name(),
        },
    )


@permission_required("core.add_user")
def user_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = UserCreateForm(request.POST, request.FILES)

        if form.is_valid():
            groups = form.cleaned_data["groups"]
            person = form.save()
            for _group in groups:
                person.groups.add(_group)
            person.save()
            LogItem.log_it(person, "CREATE", 2)
            return redirect(
                reverse("itdagene.users.user_detail", kwargs={"pk": person.pk})
            )
    else:
        form = UserCreateForm()

    return render(
        request, "users/create.html", {"form": form, "title": _("Create User")}
    )


@permission_required("core.send_welcome_email")
def send_welcome_email(request: HttpRequest, pk: Any) -> HttpResponse:
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        users_send_welcome_email(user)
        add_message(request, SUCCESS, _("The welcome email has been sent."))
        return redirect(reverse("itdagene.users.user_detail", kwargs={"pk": user.pk}))
    return render(
        request,
        "users/send_welcome_email.html",
        {
            "person": user,
            "title": _("Send welcome email"),
            "description": user.get_full_name(),
        },
    )


@login_required()
def vcard(request: HttpRequest, pk: Any) -> HttpResponse:
    try:
        if not request.user.is_staff:
            person = (
                User.objects.filter(Q(is_staff=True) | Q(id=request.user.id))
                .filter(is_active=True)
                .get(pk=pk)
            )
        else:
            person = User.objects.filter(is_active=True).order_by("username").get(pk=pk)
    except Exception:
        raise Http404

    output = vcard_string(person)
    filename = slugify(person.get_full_name())
    response = HttpResponse(output, content_type="text/x-vCard")
    response["Content-Disposition"] = f"attachment; filename={filename}"
    return response

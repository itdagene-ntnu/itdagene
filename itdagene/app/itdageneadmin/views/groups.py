from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from itdagene.app.itdageneadmin.forms import AddUserToGroupForm, GroupForm
from itdagene.core.decorators import superuser_required
from itdagene.core.log.models import LogItem
from itdagene.core.models import User


@superuser_required()
def list(request: HttpRequest) -> HttpResponse:
    groups = Group.objects.all()
    return render(
        request,
        "admin/groups/list.html",
        {"groups": groups, "title": _("Groups")},
    )


@permission_required("auth.change_group")
def view(request: HttpRequest, id_) -> HttpResponse:
    group = get_object_or_404(Group, pk=id_)
    members = User.objects.filter(groups=group)
    return render(
        request,
        "admin/groups/view.html",
        {
            "group": group,
            "members": members,
            "title": _("View Group"),
            "description": group.name,
        },
    )


@permission_required("auth.add_group")
def add(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            LogItem.log_it(group, "CREATE", 2)
            return redirect(
                reverse("itdagene.itdageneadmin.groups.view", args=[group.pk])
            )
    form = GroupForm()
    return render(
        request,
        "admin/groups/edit.html",
        {"form": form, "title": _("Add Group")},
    )


@permission_required("auth.change_group")
def edit(request: HttpRequest, id_) -> HttpResponse:
    group = get_object_or_404(Group, id=id_)
    if request.method == "POST":
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            group = form.save()
            return redirect(
                reverse("itdagene.itdageneadmin.groups.view", args=[group.pk])
            )
    form = GroupForm(instance=group)
    return render(
        request,
        "admin/groups/edit.html",
        {"form": form, "title": _("Edit Group"), "description": group.name},
    )


@permission_required("auth.change_user")
def add_user(request: HttpRequest, id_) -> HttpResponse:
    if request.method == "POST":
        group = get_object_or_404(Group, pk=id_)
        form = AddUserToGroupForm(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data["username"]
                user = User.objects.get(username=username)
                user.groups.add(group)
            except (TypeError, User.DoesNotExist):
                return HttpResponse("User does not exists", status=404)
        users = group.user_set.all()
        output = ""
        for user in users:
            output += f"<li>{user.profile}</li>"
        return HttpResponse(output)
    return HttpResponse("No post-data", status=500)

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from itdagene.app.itdageneadmin.forms import AddUserToGroupForm, GroupForm
from itdagene.core.decorators import superuser_required
from itdagene.core.log.models import LogItem
from itdagene.core.models import User


@superuser_required()
def list(request):
    groups = Group.objects.all()
    return render(
        request, "admin/groups/list.html", {"groups": groups, "title": _("Groups")}
    )


@permission_required("auth.change_group")
def view(request, id):
    group = get_object_or_404(Group, pk=id)
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
def add(request):
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
        request, "admin/groups/edit.html", {"form": form, "title": _("Add Group")}
    )


@permission_required("auth.change_group")
def edit(request, id):
    group = get_object_or_404(Group, id=id)
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
def add_user(request, id):
    if request.method == "POST":
        group = get_object_or_404(Group, pk=id)
        form = AddUserToGroupForm(request.POST)
        if form.is_valid():
            try:
                u = form.cleaned_data["username"]
                user = User.objects.get(username=u)
                user.groups.add(group)
            except (TypeError, User.DoesNotExist):
                return HttpResponse("User does not exists", status=404)
        users = group.user_set.all()
        output = ""
        for u in users:
            output += "<li>" + str(u.profile) + "</li>"
        return HttpResponse(output)

    else:
        return HttpResponse("No post-data", status=500)

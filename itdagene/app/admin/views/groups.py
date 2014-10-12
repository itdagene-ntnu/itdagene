from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from itdagene.app.admin.forms import GroupForm, AddUserToGroupForm
from django.shortcuts import render_to_response, get_object_or_404, redirect
from itdagene.core.log.models import LogItem
from django.contrib.auth.models import Group
from itdagene.core.models import User
from itdagene.app.mail.models import MailMapping
from django.shortcuts import render
from itdagene.core.decorators import superuser_required
from django.utils.translation import ugettext_lazy as _


@superuser_required()
def list (request):
    groups = Group.objects.all()
    return render(request, 'admin/groups/list.html', {'groups': groups, 'title': _('Groups')})

@permission_required('auth.change_group')
def view (request, id):
    group = get_object_or_404(Group, pk=id)
    members = User.objects.filter(groups=group)
    mail_mappings = MailMapping.get_group_mappings(group)
    return render(request, 'admin/groups/view.html', {'group': group, 'members': members, 'mail_mappings': mail_mappings, 'title':_('View Group'), 'description': group.name})

@permission_required('auth.add_group')
def add (request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            LogItem.log_it(group,'CREATE', 2)
            return redirect(reverse('itdagene.app.admin.views.groups.view', args=[group.pk]))
    form = GroupForm()
    return render(request, 'admin/groups/edit.html', {'form': form, 'title': _('Add Group')})

@permission_required('auth.change_group')
def edit (request, id):
    group = get_object_or_404(Group, id=id)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            group = form.save()
            return redirect(reverse('itdagene.app.admin.views.groups.view', args=[group.pk]))
    form = GroupForm(instance=group)
    return render(request, 'admin/groups/edit.html', {'form': form, 'title':_('Edit Group'), 'description': group.name})


@permission_required('auth.change_user')
def add_user(request, id):
    if request.method == 'POST':
        group = get_object_or_404(Group, pk=id)
        form = AddUserToGroupForm(request.POST)
        if form.is_valid():
            try:
                u = form.cleaned_data['username']
                user = User.objects.get(username=u)
                user.groups.add(group)
            except (TypeError, User.DoesNotExist):
                return HttpResponse('User does not exists', status=404)
        users = group.user_set.all()
        output = ""
        for u in users:
            output += "<li>" + str(u.profile) + "</li>"
        return HttpResponse(output)

    else:
        return HttpResponse('No post-data', status=500)

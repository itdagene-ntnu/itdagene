from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse
from itdagene.app.admin.forms import GroupForm, AddUserToGroupForm, PermissionForm
from django.shortcuts import render_to_response, get_object_or_404, redirect
from itdagene.core.log.models import LogItem
from django.contrib.auth.models import Group, User
from django.shortcuts import render

@permission_required('auth.change_group')
def list (request):
    groups = Group.objects.all()
    return render(request, 'adm/groups/list.html',
                             {'groups': groups})

@permission_required('auth.change_group')
def view (request, id):
    group = get_object_or_404(Group, pk=id)
    members = User.objects.filter(groups=group)
    form = AddUserToGroupForm()
    return render(request, 'adm/groups/view.html',
                             {'group': group,
                              'members': members,
                              'form': form})

@permission_required('auth.change_group')
def add (request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            LogItem.log_it(group,'CREATE', 2)
            return redirect(reverse('itdagene.app.admin.views.groups.view', args=[group.pk]))
    return edit(request, None)

@permission_required('auth.change_group')
def edit (request, id):
#    group = None
#    perm_forms = []
#    form = GroupForm()
#    PermFormSet = modelformset_factory(ContentType, form=PermissionForm)
#    queryset = cache.get('ctypes')
#    if not queryset:
#        queryset = ContentType.objects.exclude(app_label='auth').exclude(app_label='admin').exclude(app_label='south').exclude(app_label='session').order_by('app_label')
#        cache.set('ctypes', queryset)
#    formset = PermFormSet(queryset=queryset)
#    if id:
#        group = get_object_or_404(Group, pk=id)
#        form = GroupForm(instance=group)
#        for f in formset:
#            t = f.instance
#            for p in Permission.objects.filter(group=group):
#                if p.content_type == t:
#                    if p.action == 'CREATE': f.fields['create'] = True
#                    elif p.action == 'EDIT': f.fields['edit'] = True
#                    elif p.action == 'VIEW': f.fields['view'] = True
#                    elif p.action == 'DELETE': f.fields['delete'] = True
#    if request.method == 'POST':
#        form = GroupForm(request.POST, instance=group)
#        if form.is_valid():
#            form.save()
#            LogItem.log_it(group,'EDIT', 2)
#            return redirect(reverse('itdagene.app.admin.views.groups.view', args=[group.pk]))
    return render(request, 'adm/groups/edit.html')
#        ,
#                             {'group': group,
#                              'form': form,
#                              'formset': formset})

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

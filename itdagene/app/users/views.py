from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render
from itdagene.core.models import User
from itdagene.core.log.models import LogItem
from itdagene.core.models import Preference
from itdagene.core.profiles.models import Profile
from django.utils.translation import ugettext_lazy as _
from .forms import UserCreateForm, UserEditForm, SimpleUserEditForm, UserEditProfileAdminForm, UserEditProfileStandardForm
from django.contrib.auth.forms import PasswordChangeForm

@login_required
def user_list(request):
    persons = User.objects.filter(is_active=True).order_by('username')
    return render(request, 'users/list.html', {'persons': persons, 'title': _('User Admin')})


@login_required
def user_detail(request, pk):
    person = get_object_or_404(User, pk=pk)
    current_year = Preference.current_preference().year
    return render(request, 'users/detail.html', {'person': person, 'current_year': current_year, 'title':_('User Detail'), 'description':person.get_full_name()})


@permission_required('core.delete_user')
def user_delete(request, pk):
    person = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        person.is_active = False
        person.save()
        return redirect(reverse('app.users.views.user_list'))

    return render(request, 'users/delete.html', {'person': person, 'title': _('Delete User'), 'description':person.get_full_name()})


@login_required
def user_edit(request, pk):
    if not request.user.has_perm('core.change_user') and not request.user.pk == int(pk):
        return redirect(reverse('app.users.views.user_list'))

    person = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        if request.user.is_superuser:
            form = UserEditForm(request.POST, request.FILES, instance=person)
        else:
            form = SimpleUserEditForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            person = form.save()
            LogItem.log_it(person, 'EDIT', 2)
            return redirect(reverse('app.users.views.user_detail', args=[person.pk]))
    else:
        if request.user.is_superuser:
            form = UserEditForm(instance=person)
        else:
            form = SimpleUserEditForm(instance=person)

    return render(request, 'users/edit.html', {'form': form, 'person': person, 'title': _('Edit User'), 'description': person.get_full_name()})


@login_required
def user_edit_password(request, pk):
    if not request.user.has_perm('core.change_user') and not request.user.pk == int(pk):
        return redirect(reverse('app.users.views.user_list'))

    person = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = PasswordChangeForm(user=person, data=request.POST)

        if form.is_valid():
            form.save()
            return redirect(reverse('app.users.views.user_detail', args=[person.pk]))

    else:
        form = PasswordChangeForm(person)

    return render(request, 'users/edit_password.html', {'person': person, 'form': form, 'title': _('Change Password'), 'description': person.get_full_name()})


@permission_required('core.add_user')
def user_create(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST, request.FILES)

        if form.is_valid():
            person = form.save()
            LogItem.log_it(person, 'CREATE', 2)
            return redirect(reverse('app.users.views.user_detail', kwargs={'pk': person.pk}))
    else:
        form = UserCreateForm()

    return render(request, 'users/create.html', {'form': form, 'title': _('Create User')})










@login_required
def user_edit_profile(request, pk):
    if not request.user.has_perm('auth.change_user') and not request.user.pk == int(pk):
        return redirect(reverse('users:list'))

    person = get_object_or_404(Profile, user=pk)

    if request.method == 'POST':
        if request.user.has_perm('auth.change_user'):
            form = UserEditProfileAdminForm(request.POST, request.FILES, instance=person)
        else:
            form = UserEditProfileStandardForm(request.POST, request.FILES, instance=person)

        if form.is_valid():
            form.save()
            return redirect(reverse('users:detail', kwargs={'pk': person.user.pk}))
    else:
        if request.user.has_perm('auth.change_user'):
            form = UserEditProfileAdminForm(instance=person)
        else:
            form = UserEditProfileStandardForm(instance=person)

    return render(request, 'users/edit_profile.html', {'person': person, 'form': form})



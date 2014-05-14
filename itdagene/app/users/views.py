from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from itdagene.core.log.models import LogItem
from itdagene.core.models import Preference
from itdagene.core.profiles.models import Profile

from .forms import UserCreateForm, UserEditForm, UserEditProfileAdminForm, UserEditProfileStandardForm, \
    UserEditPasswordForm


@login_required
def user_list(request):
    persons = User.objects.filter(is_active=True).order_by('username')
    return render(request, 'users/list.html', {'persons': persons})


@permission_required('auth.add_user')
def user_create(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)

        if form.is_valid():
            person = form.save()
            LogItem.log_it(person, 'CREATE', 2)
            return redirect(reverse('users:detail', kwargs={'pk': person.pk}))
    else:
        form = UserCreateForm()

    return render(request, 'users/create.html', {'form': form})


@login_required
def user_detail(request, pk):
    person = get_object_or_404(User, pk=pk)
    current_year = Preference.current_preference().year
    return render(request, 'users/detail.html', {'person': person, 'current_year': current_year})


@login_required
def user_edit(request, pk):
    if not request.user.has_perm('auth.change_user') and not request.user.pk == int(pk):
        return redirect(reverse('users:list'))

    person = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=person)

        if form.is_valid():
            person = form.save()
            LogItem.log_it(person, 'EDIT', 2)
            return redirect(reverse('users:detail', kwargs={'pk': person.pk}))
    else:
        form = UserEditForm(instance=person)

    return render(request, 'users/edit.html', {'form': form, 'person': person})


@login_required
def user_edit_password(request, pk):
    if not request.user.has_perm('auth.change_user') and not request.user.pk == int(pk):
        return redirect(reverse('users:list'))

    person = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = UserEditPasswordForm(request.POST)

        if form.is_valid():
            old = form.data['old']
            new1 = form.data['new1']
            new2 = form.data['new2']

            if new1 == new2:
                if request.user.check_password(old):
                    person.set_password(new1)
                    person.save()

                    return reverse('users:detail', person.pk)
                else:
                    form.error_messages = 'Nytt passord stemmer ikke med bekreftet passord'
            else:
                form.error_messages = 'Det gamle passordet var ikke korrekt'
    else:
        form = UserEditPasswordForm()

    return render(request, 'users/edit_password.html', {'person': person, 'form': form})

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


@permission_required('auth.delete_user')
def user_delete(request, pk):
    person = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        person.is_active = False
        person.save()
        return redirect(reverse('users:list'))

    return render(request, 'users/delete.html', {'person': person})
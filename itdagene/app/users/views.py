from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from itdagene.core.log.models import LogItem
from itdagene.core.models import Preference

from .forms import UserCreateForm, UserEditForm


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


@permission_required('auth.delete_user')
def user_delete(request, pk):
    person = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        person.is_active = False
        person.save()
        return redirect(reverse('users:list'))

    return render(request, 'users/delete.html', {'person': person})
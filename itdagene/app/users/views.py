from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from itdagene.core.log.models import LogItem

from .forms import UserCreateForm


@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'users/list.html', {'users': users})


@permission_required('auth.add_user')
def user_create(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)

        if form.is_valid():
            user = form.save()
            LogItem.log_it(user, 'CREATE', 2)
            return redirect(reverse('users:list'))
    else:
        form = UserCreateForm()

    return render(request, 'users/create.html', {'form': form})
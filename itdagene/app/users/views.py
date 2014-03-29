from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render


@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'users/list.html', {'users': users})
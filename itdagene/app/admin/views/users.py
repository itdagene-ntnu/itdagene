from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from itdagene.app.admin.forms import UserForm, CreateUserForm, RegisterUserForm
from itdagene.core.auth import generate_password
from django.contrib.auth.decorators import permission_required
from itdagene.core.log.models import LogItem
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect
from django.db.utils import IntegrityError
from itdagene.core.models import Preference
from itdagene.core.profiles.models import Profile
from django.utils.translation import ugettext as _
from django.shortcuts import render
from django.conf import settings

@permission_required('auth.change_user')
def list (request):
    users = User.objects.filter(is_active=True).order_by('last_name')
    return render(request, 'adm/users/list.html',
                             {'users': users})
@permission_required('auth.change_user')
def list_all (request):
    users = User.objects.all().order_by('last_name')
    return render(request, 'adm/users/list.html',
                             {'users': users})

@permission_required('auth.change_user')
def add (request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            LogItem.log_it(user,'CREATE', 2)
            password = generate_password()
            user.set_password(password)
            send_mail(_('Your password for itDAGENE'),_('You have now been registered at itDAGENE.no.\n\nYour password is: ' + password),settings.FROM_ADDRESS,(user.email,))
            user.save()
            return redirect(reverse('itdagene.app.admin.views.users.view', args=[user.pk]))
    return render(request, 'adm/users/create.html',
                             {'form': form})

@permission_required('auth.change_user')
def view (request, id):
    user = get_object_or_404(User, pk=id)
    return render(request, 'adm/users/view.html',
                             {'t_user': user})

@permission_required('auth.change_user')
def edit (request, id):
    user = get_object_or_404(User, pk=id)
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            LogItem.log_it(user,'EDIT', 2)
            return redirect(reverse('itdagene.app.admin.views.users.view', args=[user.pk]))

    return render(request, 'adm/users/edit.html',
                             {'t_user': user,
                              'form': form})

@permission_required('auth.change_user')
def edit_profile (request, id):
    user = get_object_or_404(User, pk=id)
    return HttpResponsePermanentRedirect(reverse('itdagene.core.profiles.views.edit', args=[user.profile.pk]))

def register (request):
    if request.user.is_authenticated():
        return HttpResponsePermanentRedirect(reverse('itdagene.app.admin.views.users.add'))
    form = RegisterUserForm()
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone = form.cleaned_data['phone']
            if cache.get('pref'): pref = cache.get('pref')
            else:
                pref = Preference.objects.get(active=True)
                cache.set('pref', pref)
            try:
                user = User(username=username, email=username + '@stud.ntnu.no', first_name=first_name, last_name=last_name)
                user.save()
                profile = Profile(user=user, type='w', phone=phone, year=pref.year)
                profile.save()
                if user.pk and profile.pk:
                    password = generate_password()
                    user.set_password(password)
                    print unicode(profile)
                    user.save()
                    send_mail(_('Your password for itDAGENE'),_('Thank you for your registration.\n\nYour password is: ' + password),settings.FROM_ADDRESS,(user.email,))
                    return redirect(reverse('itdagene.app.frontpage.views.frontpage'))

            except IntegrityError:
                exists = True
                return render(request, 'adm/users/register.html',
                                         {'form': form,
                                          'user_already_exists': exists})

    return render(request, 'adm/users/register.html',
                             {'form': form})
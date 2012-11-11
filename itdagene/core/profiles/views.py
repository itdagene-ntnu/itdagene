from datetime import date
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, check_password
from django.core.cache import cache
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import cache_page
from itdagene.core.auth import get_current_user
from itdagene.core.profiles.forms import StandardProfileForm, PasswordForm, ProfileSearchForm, AdminProfileForm, StandardUserForm
from itdagene.core.profiles.models import Profile
from itdagene.core.search import get_query
from django.core.urlresolvers import reverse
from django.shortcuts import render
from itdagene.core.models import Preference

@cache_page
def public_profiles (request):
    if cache.get('profiles'): profiles = cache.get('profiles')
    else:
        profiles = list(Profile.objects.filter(type='b', year=Preference.current_preference().year).order_by('position__pk').select_related('position'))
        cache.set('profiles', profiles)

    if not request.user.is_authenticated():
        return render(request, 'core/profiles/profiles_public.html', {'profiles': profiles})
    else:
        return render(request, 'core/profiles/profiles.html', {'profiles': profiles})

@login_required
def profiles (request):
    if cache.get('profiles'): profiles = cache.get('profiles')
    else:
        profiles = list(Profile.objects.filter(type='b', year=date.today().year).order_by('position__pk').select_related('position'))
        cache.set('profiles', profiles)

    return render(request, 'core/profiles/profiles.html', {'profiles': profiles})

@login_required
def profile (request, id):
    profile = get_object_or_404(Profile, pk=id)
    return render(request, 'core/profiles/profile.html', {'profile': profile})

@login_required
def me(request):
    return redirect(reverse('core.profiles.views.profile', args=[request.user.profile.pk]))

@login_required
def edit_me(request):
    return redirect(reverse('core.profiles.views.edit', args=[request.user.profile.pk]))

@permission_required('profiles.change_profile')
def edit (request, id):
    profile = get_object_or_404(Profile, pk=id)
    user = profile.user
    if profile.user.id != request.user.id and not request.user.profile.is_board_member():
        return render(request, '500.html')
    if request.user.is_superuser:
        form = AdminProfileForm(instance=profile)
        user_form = StandardUserForm(instance=user)
    else:
        form = StandardProfileForm(instance=profile)
        user_form = StandardUserForm(instance=user)
    if request.method == "POST":
        if request.user.is_superuser:
            form = AdminProfileForm(request.POST, request.FILES, instance=profile)
            user_form = StandardUserForm(request.POST, request.FILES, instance=user)
        else:
            form = StandardProfileForm(request.POST, request.FILES,instance=profile)
            user_form = StandardUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid() and user_form.is_valid():
            form.save()
            user_form.save()
            request.session['django_language'] = get_current_user().profile.language

    return render(request, 'core/profiles/form.html',
                             {'form': form,
                              'user_form': user_form,
                              'form_title':_('Change your profile')})

#@login_required
#def group_vcard(request):
#    """
#    View function for returning group vcard
#    """
#    all = User.objects.order_by('lastname', 'firstname')
#    output = '\n'.join(_vcard_string(one) for one in all)
#    response = HttpResponse(output, mimetype="text/x-vCard")
#    response['Content-Disposition'] = 'attachment; filename=example_org_people.vcf'
#    return response

@login_required
def change_password(request):
    form = PasswordForm()
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            old = form.data['old']
            new1 = form.data['new1']
            new2 = form.data['new2']
            if new1 == new2:
                if request.user.check_password(old):
                    user = request.user
                    user.set_password(new1)
                    user.save()
                    return me(request)
                else:
                    form.error_messages = _('The passwords do not match.')
            else:
                form.error_messages = _('The old password is incorrect.')

    return render(request, 'core/profiles/change_password.html',
                             {'form': form})



@permission_required('profiles.change_profile')
def search (request):
    search_form = ProfileSearchForm(request.GET)
    if search_form.is_valid():
        q = search_form.data['q']
        query = get_query(q,['first_name', 'last_name'])
        search_result = User.objects.filter(query)

        return render(request, 'core/profiles/search_result.html',
                                 {'search_result': search_result,
                                  'search_form': search_form,
                                  'query': q})

    return render(request, 'core/profiles/search_result.html',
                                 {'search_result': None,
                                  'search_form': search_form,
                                  'query': None})

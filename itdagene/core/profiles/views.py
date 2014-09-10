from django.core.cache import cache
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from itdagene.core.models import Preference
from itdagene.core.profiles.models import Profile

def public_profiles (request):
    if cache.get('profiles'): profiles = cache.get('profiles')
    else:
        profiles = list(Profile.objects.filter(type='b', year=Preference.current_preference().year).order_by('position__pk').select_related('position'))
        cache.set('profiles', profiles)

    if not request.user.is_authenticated():
        return render(request, 'core/profiles/profiles_public.html', {'profiles': profiles})
    else:
        return render(request, 'core/profiles/profiles.html', {'profiles': profiles})

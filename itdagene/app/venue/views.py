from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy
from itdagene.app.venue.forms import StandForm
from itdagene.app.venue.models import Stand
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

@permission_required('venue.change_stand')
def venue(request):
    stands = Stand.objects.all()
    return render(request, 'venue/base.html',
                             {'stands': stands})
@permission_required('venue.change_stand')
def stands(request):
    stands = None
    if request.user.profile.type == 'b':
        stands = cache.get('standsforuser' + str(request.user.pk))
        if not stands: stands = create_stand_cache(request)
    #elif request.user.profile.type == 'c':
        #stands = Stand.objects.filter()
    else:
        raise Http404
    return render(request, 'venue/stands.html',
                             {'stands': stands})
@permission_required('venue.change_stand')
def edit_stand(request, id=None):
    form = StandForm()
    title = ugettext_lazy('Add stand')
    if id:
        pass
    if request.method == 'POST':
        form = StandForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('venue'))

    return render(request, 'venue/form.html', {'form': form, 'title': title})

def create_stand_cache(request):
    stands = Stand.objects.filter(company_day1__contact=request.user,company_day2__contact=request.user).select_related('user', 'package')
    cache.set('standsforuser' + str(request.user.pk), list(stands))
    return stands

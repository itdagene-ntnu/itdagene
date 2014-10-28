from django.core.cache import cache
from itdagene.core.decorators import staff_required
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy
from itdagene.app.venue.forms import StandForm
from itdagene.app.venue.models import Stand
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _


@staff_required()
def venue(request):
    stands = Stand.objects.all()
    user_stands = Stand.objects.filter(stand_companies__company__contact=request.user)
    return render(request, 'venue/base.html', {'stands': stands, 'user_stands': user_stands,
                                               'title': _('Venue')})


@staff_required()
def view_stand(request, pk):
    pass


@permission_required('venue.add_stand')
def add_stand(request):
    pass


@permission_required('venue.change_stand')
def edit_stand(request, id=None):
    pass


@permission_required('venue.delete_stand')
def delete_stand(request, id=None):
    pass


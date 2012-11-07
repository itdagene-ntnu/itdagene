from itdagene.core.decorators import staff_or_404
from itdagene.core.search import get_query
from itdagene.app.meetings.forms import MeetingForm, SearchForm
from itdagene.app.meetings.models import Meeting, ReplyMeeting, Penalty
from django.contrib.auth.decorators import permission_required, login_required
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache
from django.shortcuts import render
from itdagene.core.shortcuts import send_language_specific_mail

from django.contrib.auth.models import User

@permission_required('meetings.change_meeting')
def list (request):
    meetings = Meeting.objects.all().order_by('date')
    penalties = Penalties()
    search_form = SearchForm()
    return render(request, 'meetings/base.html',
                             {'meetings': meetings,
                              'penalties': penalties,
                              'search_form': search_form})

@permission_required('meetings.change_meeting')
def meeting (request, id):
    meeting = get_object_or_404(Meeting, pk=id)
    try:
        reply = ReplyMeeting.objects.get(meeting=meeting, user=request.user)
    except (TypeError, ReplyMeeting.DoesNotExist):
        reply = None
    return render(request, 'meetings/view.html',
                                 {'meeting': meeting,
                                  'reply': reply})

@permission_required('meetings.change_meeting')
def search(request):
    result = None
    query = ""

    query = request.GET.get('query')
    form = SearchForm(request.GET)

    if query:
        query_filter = get_query(query, ['abstract'])
        result = Meeting.objects.filter(query_filter)
    return render(request, 'meetings/search.html', {'result': result, 'search_form': form})


@permission_required('meetings.change_meeting')
def add (request):
    return edit(request)

@permission_required('meetings.change_meeting')
def edit (request, id=False):

    if id:
        meeting = get_object_or_404(Meeting, pk=id)
        form = MeetingForm(instance=meeting)
        form_title = _('Edit meeting')

    else:
        meeting = None
#        if Meeting.objects.filter(type=0).count():
#            last = Meeting.objects.filter(type=0).order_by('date').reverse()[0].referee
#
#            if User.objects.exclude(pk=5).filter(is_active=True, profile__type='b', pk__gt=last.pk).order_by('id').count():
#                referee = User.objects.exclude(pk=5).filter(is_active=True, profile__type='b', pk__gt=last.pk).order_by('id')[0]
#            else:
#                referee = User.objects.exclude(pk=5).filter(is_active=True, profile__type='b').order_by('id')
#
#            meeting = Meeting(referee=referee)
        form = MeetingForm(instance=meeting)
        form_title = _('Add meeting')

    if request.method == 'POST':

        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            meeting = form.save()
            return redirect(reverse('app.meetings.views.meeting', args=[meeting.pk]))

    return render(request, 'meetings/form.html',
                             {'meeting': meeting,
                              'form': form,
                              'form_title': form_title})

@login_required
def attend(request, id):
    reply = get_object_or_404(ReplyMeeting, meeting__pk=id, user=request.user)
    reply.is_attending = True
    reply.save()
    return redirect(reverse('app.meetings.views.meeting', args=[reply.meeting.pk]))

@login_required
def not_attend(request, id):
    reply = get_object_or_404(ReplyMeeting, meeting__pk=id, user=request.user)
    reply.is_attending = False
    reply.save()
    return redirect(reverse('app.meetings.views.meeting', args=[reply.meeting.pk]))

@staff_or_404
def send_invites(request, id):
    meeting = get_object_or_404(Meeting, pk=id)
    replies = ReplyMeeting.objects.filter(meeting__pk=id)

    users = [r.user for r in replies]
    send_language_specific_mail('Meeting invite', users, 'emails/meeting_invite.html', {'meeting': meeting})
    return render(request, 'meetings/send_invites.html',
                              {'invited': replies})

class Penalties:
    def __init__(self):
        self.beer = cache.get('totalpenaltiesbeer')
        self.wine = cache.get('totalpenaltieswine')
        if not self.beer:
            self.beer = 0
            for p in Penalty.objects.filter(type='beer'):
                self.beer += p.bottles
            cache.set('totalpenaltiesbeer', self.beer)

        if not self.wine:
            self.wine = 0
            for p in Penalty.objects.filter(type='wine'):
                self.wine += p.bottles
            cache.set('totalpenaltieswine', self.wine)

        beer_users = []
        for u in User.objects.filter(profile__type='b'):
            count = sum([p.bottles for p in u.penalties.filter(type='beer')])
            if count: beer_users.append({'name': u.profile, 'number': count})
        self.beer_list_users = beer_users

        wine_users = []
        for u in User.objects.filter(profile__type='b'):
            count = sum([p.bottles for p in u.penalties.filter(type='wine')])
            if count: wine_users.append({'name': u.profile, 'number': count})
        self.wine_list_users = wine_users


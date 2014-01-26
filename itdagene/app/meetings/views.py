from itdagene.core import Preference
from itdagene.core.decorators import staff_or_404
from itdagene.core.profiles.models import Profile
from itdagene.core.search import get_query
from itdagene.app.meetings.forms import MeetingForm, SearchForm, PenaltyForm
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
def list(request):
    meeting_lists = []
    penalty_lists = []
    for pref in Preference.objects.all().order_by('-year'):
        meeting_lists.append((pref.year, Meeting.objects.filter(date__year=pref.year).order_by('-date')))
        penalty_lists.append(Penalties(pref.year))

    search_form = SearchForm()
    return render(request, 'meetings/base.html',
                             {'meeting_lists': meeting_lists,
                              'penalty_lists': penalty_lists,
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
            return redirect(reverse('itdagene.app.meetings.views.meeting', args=[meeting.pk]))

    return render(request, 'meetings/form.html',
                             {'meeting': meeting,
                              'form': form,
                              'form_title': form_title})

@permission_required('meetings.change_meeting')
def add_penalties(request, id):
    form = PenaltyForm()
    if id:
        meeting = get_object_or_404(Meeting, pk=id)
        form = PenaltyForm()
        if request.method == 'POST':
            form = PenaltyForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect(reverse('itdagene.app.meetings.views.meeting', args=[meeting.pk]))

    return render(request, 'meetings/penalty_form.html', {'form':form})

@login_required
def attend(request, id):
    reply = get_object_or_404(ReplyMeeting, meeting__pk=id, user=request.user)
    reply.is_attending = True
    reply.save()
    return redirect(reverse('itdagene.app.meetings.views.meeting', args=[reply.meeting.pk]))

@login_required
def not_attend(request, id):
    reply = get_object_or_404(ReplyMeeting, meeting__pk=id, user=request.user)
    reply.is_attending = False
    reply.save()
    return redirect(reverse('itdagene.app.meetings.views.meeting', args=[reply.meeting.pk]))

@staff_or_404
def send_invites(request, id):
    meeting = get_object_or_404(Meeting, pk=id)
    replies = ReplyMeeting.objects.filter(meeting__pk=id)

    users = [r.user for r in replies]
    send_language_specific_mail('Meeting invite', users, 'emails/meeting_invite.html', {'meeting': meeting})
    return render(request, 'meetings/send_invites.html',
                              {'invited': replies})

class Penalties:
    def __init__(self, year):
        self.year = year
        self.beer = 0
        self.wine = 0

        beer_users = []
        wine_users = []
        print self.year
        for profile in Profile.objects.filter(type='b', year=self.year):
            count = sum([p.bottles for p in profile.user.penalties.filter(type='beer')])
            if count:
                beer_users.append({'name': profile, 'number': count})
                self.beer += count

            count = sum([p.bottles for p in profile.user.penalties.filter(type='wine')])
            if count:
                wine_users.append({'name': profile, 'number': count})
                self.wine += count

        self.beer_list_users = beer_users
        self.wine_list_users = wine_users
from django.contrib.auth.decorators import permission_required
from django.contrib.messages import SUCCESS, add_message
from django.shortcuts import Http404, get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from itdagene.app.mail.tasks import meeting_send_invite
from itdagene.app.meetings.forms import MeetingForm, PenaltyForm
from itdagene.app.meetings.models import Meeting, ReplyMeeting
from itdagene.core.decorators import staff_required
from itdagene.core.models import Preference, User


@staff_required()
def list(request):
    meeting_lists = []
    penalty_lists = []
    year_list = []
    for pref in Preference.objects.all().order_by("-year"):
        year_list.append(pref.year)
        meeting_lists.append(
            (pref.year, Meeting.objects.filter(preference=pref).order_by("-date"))
        )
        penalty_lists.append(Penalties(pref.year))

    return render(
        request,
        "meetings/list.html",
        {
            "meeting_lists": meeting_lists,
            "penalty_lists": penalty_lists,
            "year_list": year_list,
            "title": _("Meetings"),
        },
    )


@permission_required("meetings.add_meeting")
def add(request):
    form = MeetingForm()
    if request.method == "POST":
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save()
            meeting.preference = Preference.current_preference()
            meeting.save()
            add_message(request, SUCCESS, _("Meeting added."))
            return redirect(reverse("itdagene.meetings.list"))
    return render(
        request, "meetings/form.html", {"form": form, "title": _("Add Meeting")}
    )


@staff_required()
def meeting(request, id):
    meeting = get_object_or_404(Meeting, pk=id)
    try:
        reply = ReplyMeeting.objects.get(meeting=meeting, user=request.user)
    except (TypeError, ReplyMeeting.DoesNotExist):
        reply = None
    return render(
        request,
        "meetings/view.html",
        {
            "meeting": meeting,
            "reply": reply,
            "title": _("Meeting"),
            "description": meeting,
        },
    )


@permission_required("meetings.change_meeting")
def add_penalties(request, id):
    if id:
        meeting = get_object_or_404(Meeting, pk=id)
        form = PenaltyForm()
        if request.method == "POST":
            form = PenaltyForm(request.POST)
            if form.is_valid():
                penalty = form.save(commit=False)
                penalty.meeting = meeting
                penalty.save()
                return redirect(reverse("itdagene.meetings.meeting", args=[meeting.pk]))
        return render(
            request,
            "meetings/form.html",
            {
                "meeting": meeting,
                "form": form,
                "title": _("Add Penalties"),
                "description": str(meeting),
            },
        )
    raise Http404


@staff_required()
def send_invites(request, id):
    meeting = get_object_or_404(Meeting, pk=id)
    replies = ReplyMeeting.objects.filter(meeting__pk=id, is_attending=None)
    users = [r.user for r in replies]
    meeting_send_invite.delay(users, meeting)
    add_message(request, SUCCESS, _("All participants will receive a mail shortly."))
    return redirect(reverse("itdagene.meetings.meeting", args=[meeting.pk]))


@staff_required()
def attend(request, id):
    reply = get_object_or_404(ReplyMeeting, meeting__pk=id, user=request.user)
    reply.is_attending = True
    reply.save()
    return redirect(reverse("itdagene.meetings.meeting", args=[reply.meeting.pk]))


@staff_required()
def not_attend(request, id):
    reply = get_object_or_404(ReplyMeeting, meeting__pk=id, user=request.user)
    reply.is_attending = False
    reply.save()
    return redirect(reverse("itdagene.meetings.meeting", args=[reply.meeting.pk]))


@permission_required("meetings.change_meeting")
def edit(request, id=False):
    meeting = get_object_or_404(Meeting, pk=id)
    form = MeetingForm(instance=meeting)
    if request.method == "POST":
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            meeting = form.save()
            return redirect(reverse("itdagene.meetings.meeting", args=[meeting.pk]))

    return render(
        request,
        "meetings/form.html",
        {
            "meeting": meeting,
            "form": form,
            "title": _("Edit Meeting"),
            "description": str(meeting),
        },
    )


class Penalties:
    def __init__(self, year):
        self.year = year
        self.beer = 0
        self.wine = 0

        beer_users = []
        wine_users = []

        for user in User.objects.filter(year=year):
            count = sum([p.bottles for p in user.penalties.filter(type="beer")])
            if count:
                beer_users.append({"name": user.get_full_name(), "number": count})
                self.beer += count

            count = sum([p.bottles for p in user.penalties.filter(type="wine")])
            if count:
                wine_users.append({"name": user.get_full_name(), "number": count})
                self.wine += count

        self.beer_list_users = beer_users
        self.wine_list_users = wine_users

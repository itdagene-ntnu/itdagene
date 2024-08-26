from typing import Any, List

from django.contrib.auth.decorators import permission_required
from django.contrib.messages import SUCCESS, add_message
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from itdagene.app.mail.tasks import meeting_send_invite
from itdagene.app.meetings.forms import MeetingForm, PenaltyForm
from itdagene.app.meetings.models import Meeting, ReplyMeeting
from itdagene.core.decorators import staff_required
from itdagene.core.models import Preference, User


@staff_required()
def list(request: HttpRequest) -> HttpResponse:
    meeting_lists: List = []
    penalty_lists: List[Penalties] = []
    year_list: List[int] = []
    for pref in Preference.objects.all().order_by("-year"):
        year_list.append(pref.year)
        meeting_lists.append(
            (
                pref.year,
                Meeting.objects.filter(preference=pref).order_by("-date"),
            )
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
def add(request: HttpRequest) -> HttpResponse:
    form = MeetingForm()
    if request.method == "POST":
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting_ = form.save()
            meeting_.preference = Preference.current_preference()
            meeting_.save()
            add_message(request, SUCCESS, _("Meeting added."))
            return redirect(reverse("itdagene.meetings.list"))
    return render(
        request,
        "meetings/form.html",
        {"form": form, "title": _("Add Meeting")},
    )


@staff_required()
def meeting(request: HttpRequest, id: Any) -> HttpResponse:
    meeting_ = get_object_or_404(Meeting, pk=id)
    try:
        reply = ReplyMeeting.objects.get(meeting=meeting_, user=request.user)
    except (TypeError, ReplyMeeting.DoesNotExist):
        reply = None
    return render(
        request,
        "meetings/view.html",
        {
            "meeting": meeting_,
            "reply": reply,
            "title": _("Meeting"),
            "description": meeting_,
        },
    )


@permission_required("meetings.change_meeting")
def add_penalties(request: HttpRequest, id: Any) -> HttpResponse:
    if id:
        meeting_ = get_object_or_404(Meeting, pk=id)
        form = PenaltyForm()
        if request.method == "POST":
            form = PenaltyForm(request.POST)
            if form.is_valid():
                penalty = form.save(commit=False)
                penalty.meeting = meeting_
                penalty.save()
                return redirect(
                    reverse("itdagene.meetings.meeting", args=[meeting_.pk])
                )
        return render(
            request,
            "meetings/form.html",
            {
                "meeting": meeting_,
                "form": form,
                "title": _("Add Penalties"),
                "description": str(meeting_),
            },
        )
    raise Http404


@staff_required()
def send_invites(request: HttpRequest, id: Any) -> HttpResponse:
    meeting_ = get_object_or_404(Meeting, pk=id)
    replies = ReplyMeeting.objects.filter(meeting__pk=id, is_attending=None)
    users = [r.user for r in replies]
    meeting_send_invite.delay(users, meeting_)
    add_message(request, SUCCESS, _("All participants will receive a mail shortly."))
    return redirect(reverse("itdagene.meetings.meeting", args=[meeting_.pk]))


@staff_required()
def attend(request: HttpRequest, id: Any) -> HttpResponse:
    reply = get_object_or_404(ReplyMeeting, meeting__pk=id, user=request.user)
    reply.is_attending = True
    reply.save()
    return redirect(reverse("itdagene.meetings.meeting", args=[reply.meeting.pk]))


@staff_required()
def not_attend(request: HttpRequest, id: Any) -> HttpResponse:
    reply = get_object_or_404(ReplyMeeting, meeting__pk=id, user=request.user)
    reply.is_attending = False
    reply.save()
    return redirect(reverse("itdagene.meetings.meeting", args=[reply.meeting.pk]))


@permission_required("meetings.change_meeting")
def edit(request: HttpRequest, id: Any = False) -> HttpResponse:
    meeting_ = get_object_or_404(Meeting, pk=id)
    form = MeetingForm(instance=meeting_)
    if request.method == "POST":
        form = MeetingForm(request.POST, instance=meeting_)
        if form.is_valid():
            meeting_ = form.save()
            return redirect(reverse("itdagene.meetings.meeting", args=[meeting_.pk]))
    return render(
        request,
        "meetings/form.html",
        {
            "meeting": meeting_,
            "form": form,
            "title": _("Edit Meeting"),
            "description": str(meeting_),
        },
    )


class Penalties:
    def __init__(self, year) -> None:
        self.year = year
        self.beer = 0
        self.wine = 0

        beer_users = []
        wine_users = []

        for user in User.objects.filter(year=year):
            count = sum(p.bottles for p in user.penalties.filter(type="beer"))
            if count:
                beer_users.append({"name": user.get_full_name(), "number": count})
                self.beer += count

            count = sum(p.bottles for p in user.penalties.filter(type="wine"))
            if count:
                wine_users.append({"name": user.get_full_name(), "number": count})
                self.wine += count

        self.beer_list_users = beer_users
        self.wine_list_users = wine_users

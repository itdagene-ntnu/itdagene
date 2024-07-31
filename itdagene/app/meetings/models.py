import datetime

from django.conf import settings
from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    DateField,
    ForeignKey,
    PositiveIntegerField,
    TextField,
    TimeField,
)
from django.urls import reverse
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from itdagene.core.log.models import LogItem
from itdagene.core.models import BaseModel, Preference, User


MEETING_TYPES = (
    (0, _("Board meeting")),
    (1, _("Web")),
    (2, _("Banquet")),
    (3, _("Logistics")),
    (4, _("Marketing")),
    (5, _("Other")),
)


class Meeting(BaseModel):
    date = DateField(verbose_name=_("date"))
    start_time = TimeField(verbose_name=_("from time"))
    end_time = TimeField(blank=True, null=True, verbose_name=_("to time"))
    type = PositiveIntegerField(
        choices=MEETING_TYPES, default=0, verbose_name=_("type")
    )
    location = CharField(max_length=40, blank=True, verbose_name=_("location"))
    agenda = TextField(blank=True, null=True, verbose_name=_("Meeting Agenda"))
    abstract = TextField(blank=True, null=True, verbose_name=_("abstract"))
    is_board_meeting = BooleanField(default=True, verbose_name=_("is board meeting"))
    referee = ForeignKey(
        User,
        related_name="refereed_meetings",
        on_delete=SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("referee"),
    )
    preference = ForeignKey(
        Preference,
        on_delete=SET_NULL,
        verbose_name="Preference",
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return self.get_type_display()

    def save(self, *args, **kwargs) -> None:
        super(Meeting, self).save(*args, **kwargs)

    def attending(self) -> list:
        att = list(self.replies.filter(is_attending=True))
        return att

    def not_attending(self) -> list:
        att = list(self.replies.filter(is_attending=False))
        return att

    def awaiting_reply(self) -> list:
        att = list(self.replies.filter(is_attending=None))
        return att

    def attending_link(self) -> str:
        return (
            f"http://{settings.SITE['domain']}"
            f"{reverse('itdagene.meetings.attend', args=[self.pk])}"
        )

    def not_attending_link(self) -> str:
        return (
            f"http://{settings.SITE['domain']}"
            f"{reverse('itdagene.meetings.not_attend', args=[self.pk])}"
        )

    def get_absolute_url(self) -> str:
        return reverse("itdagene.meetings.meeting", args=(self.pk,))

    def get_start_date(self) -> datetime.datetime:
        return datetime.datetime.combine(self.date, self.start_time)

    def get_end_date(self) -> datetime.datetime:
        return datetime.datetime.combine(self.date, self.end_time)

    class Meta:
        verbose_name = _("meeting")
        verbose_name_plural = _("meetings")


class ReplyMeeting(BaseModel):
    meeting = ForeignKey(
        Meeting,
        related_name="replies",
        verbose_name=_("meeting"),
        on_delete=CASCADE,
    )
    user = ForeignKey(User, verbose_name=_("user"), on_delete=CASCADE)
    is_attending = BooleanField(verbose_name=_("attending"), null=True, blank=True)

    def __str__(self) -> str:
        return gettext("Meeting participation: %(user)s") % {"user": str(self.user)}

    def get_absolute_url(self) -> str:
        return reverse("itdagene.meetings.meeting", args=(self.meeting.pk,))

    def save(self, *args, **kwargs) -> None:
        super(ReplyMeeting, self).save()


class Penalty(BaseModel):
    TYPES = (("beer", _("Beer")), ("wine", _("Wine")))
    user = ForeignKey(
        User,
        related_name="penalties",
        verbose_name=_("person"),
        on_delete=CASCADE,
    )
    meeting = ForeignKey(
        Meeting,
        blank=True,
        null=True,
        verbose_name=_("meeting"),
        on_delete=SET_NULL,
    )
    type = CharField(
        max_length=10, default="beer", choices=TYPES, verbose_name=_("type")
    )
    bottles = PositiveIntegerField(default=2, verbose_name=_("number of bottles"))
    reason = TextField(verbose_name=_("reason"))

    def __str__(self) -> str:
        return f"{self.user.username} {self.bottles} {self.get_type_display()}"

    def save(self, *args, **kwargs) -> None:
        action = "EDIT" if self.pk else "CREATE"
        super(Penalty, self).save(*args, **kwargs)
        LogItem.log_it(self, action, 1)

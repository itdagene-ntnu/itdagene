from django.db.models import (
    CASCADE,
    SET_NULL,
    BooleanField,
    CharField,
    DateField,
    EmailField,
    ForeignKey,
    ImageField,
    PositiveIntegerField,
    TextField,
    TimeField,
)
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from itdagene.app.company.models import Company
from itdagene.app.stands.models import DigitalStand
from itdagene.core.models import BaseModel


EVENT_TYPES = (
    (0, _("Course")),
    (1, _("Company presentation")),
    (2, _("Banquet")),
    (3, _("Summer internship marathon")),
    (4, _("Baloon drop")),
    (5, _("Competition")),
    (6, _("Other")),
    (7, _("Promoted company event")),
)


class Event(BaseModel):
    title = CharField(max_length=80, verbose_name=_("title"))
    date = DateField(verbose_name=_("date"))
    time_start = TimeField(verbose_name=_("start time"))
    time_end = TimeField(verbose_name=_("end time"))
    description = TextField(verbose_name=_("description"))
    type = PositiveIntegerField(choices=EVENT_TYPES, verbose_name=_("type"))
    location = CharField(max_length=30, verbose_name=_("location"))
    cover_image = ImageField(upload_to="event_covers/", default=None, blank=True, null=True, verbose_name=_("cover image"))
    is_internal = BooleanField(verbose_name=_("internal event"), default=False)
    company = ForeignKey(
        Company,
        null=True,
        on_delete=SET_NULL,
        blank=True,
        verbose_name=_("hosting company"),
    )
    uses_tickets = BooleanField(verbose_name=_("uses tickets"), default=False)
    max_participants = PositiveIntegerField(
        null=True, blank=True, verbose_name=_("max nr of participants")
    )
    stand = ForeignKey(
        DigitalStand,
        null=True,
        on_delete=SET_NULL,
        blank=True,
        verbose_name=_("Associated stand"),
    )

    def __str__(self) -> str:
        return str(self.title)

    def get_absolute_url(self) -> str:
        return reverse("itdagene.events.view_event", args=[self.pk])


class Ticket(BaseModel):
    event = ForeignKey(
        Event,
        related_name="tickets",
        on_delete=CASCADE,
        verbose_name=_("event"),
    )
    company = ForeignKey(
        Company,
        related_name="tickets",
        on_delete=SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("company"),
    )
    first_name = CharField(_("first name"), max_length=30, blank=True)
    last_name = CharField(_("last name"), max_length=30, blank=True)
    email = EmailField(_("e-mail address"), blank=True)

    class Meta:
        ordering = ("last_name",)

    def __str__(self) -> str:
        return f"{self.event.title}: {self.full_name()}"

    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

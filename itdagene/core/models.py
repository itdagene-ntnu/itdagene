from datetime import datetime
from typing import Any

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    ForeignKey,
    ImageField,
    IntegerField,
    Model,
    PositiveIntegerField,
    TextField,
    URLField,
)
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from raven.breadcrumbs import record
from social_core.exceptions import AuthForbidden

from itdagene.core.auth import get_current_user


def user_default_year() -> int:
    # Users are always created the year "before" they are active
    return now().year + 1


def auth_allowed(backend, details: dict, response, *args, **kwargs) -> None:
    record(message="Starting social auth", category="authentication", data=details)
    if not backend.auth_allowed(response, details):
        raise AuthForbidden(backend)


def get_user(backend, details: dict, user: Any = None, *args, **kwargs) -> dict:
    try:
        return dict(kwargs, user=User.objects.get(email=details["email"]))
    except Exception as exc:
        raise AuthForbidden(backend) from exc


class User(AbstractUser):
    phone = IntegerField(blank=True, null=True, verbose_name=_("phone number"))
    linkedin = CharField(
        max_length=255, blank=True, null=True, verbose_name=_("LinkedIn")
    )
    photo = ImageField(
        upload_to="photos/users/",
        blank=True,
        null=True,
        verbose_name=_("Photo"),
    )
    language = CharField(
        max_length=3,
        default=settings.DEFAULT_LANGUAGE,
        choices=settings.LANGUAGES,
        verbose_name=_("Language"),
    )
    mail_notification = BooleanField(
        default=True, verbose_name=_("Send mail notifications")
    )
    year = PositiveIntegerField(
        verbose_name=_("Active Year"),
        help_text=_("Year the user was active."),
        default=user_default_year,
        blank=True,
        null=True,
    )

    class Meta(AbstractUser.Meta):
        permissions = (("send_welcome_email", "Can send welcome emails"),)

    def get_absolute_url(self) -> str:
        return reverse("itdagene.users.user_detail", args=[self.pk])

    def __str__(self) -> str:
        if self.get_full_name():
            return self.get_full_name()
        return self.username

    @property
    def full_name(self) -> str:
        return self.get_full_name()

    def role(self) -> str:
        for group in self.groups.all():
            if group.name != "Styret":
                return group
        return ""


class BaseModel(Model):
    creator = ForeignKey(
        User,
        editable=False,
        related_name="%(class)s_creator",
        on_delete=CASCADE,
    )
    saved_by = ForeignKey(
        User,
        editable=False,
        related_name="%(class)s_saved_by",
        on_delete=CASCADE,
    )
    date_created = DateTimeField(editable=False)
    date_saved = DateTimeField(editable=False)

    def __str__(self) -> str:
        return f"{self.creator.username} {self.id}"

    def save(
        self,
        notify_subscribers: bool = True,
        log_it: bool = True,
        log_priority: int = 0,
        *args,
        **kwargs,
    ) -> None:
        user = get_current_user()
        action = "EDIT" if self.pk else "CREATE"

        if not user or not user.is_authenticated:
            user = User.objects.filter(is_superuser=True).first()

        if not self.pk:
            self.creator = user
            self.date_created = now()

        self.saved_by = user
        self.date_saved = now()

        super(BaseModel, self).save(*args, **kwargs)

        # Problems when top-layer import from core/notifications/models.py
        from itdagene.core.notifications.models import Subscription

        Subscription.subscribe(self, user)

        if notify_subscribers:
            Subscription.notify_subscribers(self)

        if log_it:
            # Problems when top-layer import from core/notifications/models.py
            from itdagene.core.log.models import LogItem

            LogItem.log_it(self, action, log_priority)

    def get_absolute_url(self) -> str:
        c_type = ContentType.objects.get_for_model(self)
        return f"/{c_type.app_label}/{c_type}s/{self.pk}/"

    def notification_priority(self) -> int:
        return 1

    def notification_message(self) -> str:
        return f"{self} was changed"

    def notification_object(self) -> Model:
        return self

    class Meta:
        abstract = True

    @classmethod
    def exclude_fields(cls) -> None:
        return None


class Preference(BaseModel):
    development_mode = BooleanField(
        default=False,
        verbose_name=_("Development Mode"),
        help_text=_(
            "This option puts the site in development mode. The public page "
            "will be disabled."
        ),
    )

    active = BooleanField(verbose_name=_("active"), default=False)
    year = IntegerField(blank=True, null=True, verbose_name=_("year"))
    start_date = DateField(verbose_name=_("start date"))
    end_date = DateField(verbose_name=_("end date"))
    nr_of_stands = PositiveIntegerField(
        default=30,
        verbose_name=_("number of stands"),
        help_text=_("This is for each day, not the sum of each day"),
    )
    view_sp = BooleanField(
        verbose_name=_("view partners"),
        help_text=_("Should all collaborators be displayed on the front page?"),
        default=False,
    )
    view_hsp = BooleanField(
        verbose_name=_("view main collaborator"),
        help_text=_("Should the main collaborator be displayed on the front page?"),
        default=False,
    )
    view_companies = BooleanField(
        verbose_name=_("view all comapnies"),
        help_text=_("Should all companies be displayed on the front page?"),
        default=False,
    )
    hsp_intro = TextField(
        null=False,
        blank=True,
        default="",
        verbose_name=_("Main collaborator introduction"),
        help_text=_(
            "Introduction of main collaborator to be displayed above video on "
            "front page"
        ),
    )
    hsp_video = URLField(
        null=True,
        blank=True,
        verbose_name=_("Main collaborator video URL"),
        help_text=_("URL to the video introduction of main collaborator"),
    )
    hsp_poster = URLField(
        null=True,
        blank=True,
        verbose_name=_("Main collaborator poster URL"),
        help_text=_("URL to the image to display before video is played"),
    )

    show_interest_form = BooleanField(
        verbose_name=_("Show interest form"),
        help_text=_(
            "Should the company participation interest form be visible on the "
            "front page?"
        ),
        default=True,
    )

    interest_form_url = URLField(
        verbose_name=_("Interest form URL"),
        help_text=_("What is the URL to the company participation interest form?"),
        default="https://interesse.itdagene.no",
    )

    def __str__(self) -> str:
        return str(self.year)

    def save(self, *args, **kwargs) -> None:
        kwargs["log_it"] = True
        kwargs["log_priority"] = 3
        super(Preference, self).save(*args, **kwargs)

        if self.active:
            cache.set("pref", self)

    class Meta:
        verbose_name = _("Preference")
        verbose_name_plural = _("Preferences")

    @classmethod
    def current_preference(cls) -> BaseModel:
        if cache.get("pref") is not None:
            return cache.get("pref")
        try:
            pref = Preference.objects.get(active=True)
        except Preference.DoesNotExist:
            year = now().year
            pref, _ = Preference.objects.get_or_create(
                year=year,
                defaults={
                    "active": True,
                    "start_date": datetime.strptime(f"{year}-09-11", "%Y-%m-%d"),
                    "end_date": datetime.strptime(f"{year}-09-12", "%Y-%m-%d"),
                },
            )
            pref.active = True
            pref.save(notify_subscribers=False, log_it=False)
        cache.set("pref", pref)
        return pref

    @classmethod
    def get_preference_by_year(cls, year: int) -> BaseModel:
        try:
            return cls.objects.get(year=int(year), active=True)
        except cls.DoesNotExist:
            year = now().year
            pref, _ = Preference.objects.get_or_create(
                year=year,
                defaults={
                    "active": True,
                    "start_date": datetime.strptime(f"{year}-09-11", "%Y-%m-%d"),
                    "end_date": datetime.strptime(f"{year}-09-12", "%Y-%m-%d"),
                },
            )
            pref.active = True
            pref.save(notify_subscribers=False, log_it=False)
            return pref

    def get_absolute_url(self) -> str:
        return reverse("itdagene.itdageneadmin.preferences.edit")

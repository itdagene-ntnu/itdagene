from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateTimeField,
    ForeignKey,
    ImageField,
    Manager,
    ManyToManyField,
    PositiveIntegerField,
    SlugField,
    TextField,
    URLField,
)
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from itdagene.app.career.managers import JoblistingManager
from itdagene.app.company.models import Company, CompanyContact
from itdagene.core.models import BaseModel


class Town(BaseModel):
    name = CharField(max_length=100, verbose_name=_("name"))

    def __str__(self) -> str:
        return str(self.name)


class Joblisting(BaseModel):
    active_objects = JoblistingManager()
    objects = Manager()

    class DisplayedJoblistingManager(JoblistingManager):
        def get_queryset(self):
            return super().to_display()

    displayed_objects = DisplayedJoblistingManager()

    JOB_TYPES = (
        ("si", _("Summer internship")),
        ("pp", _("Permanent position")),
        ("ot", _("Other")),
    )

    company = ForeignKey(
        Company,
        related_name="joblistings",
        verbose_name=_("company"),
        on_delete=CASCADE,
    )
    title = CharField(max_length=160, verbose_name=_("title"))
    type = CharField(max_length=20, choices=JOB_TYPES, verbose_name=_("type"))
    description = TextField(verbose_name=_("Description"))
    contact = ForeignKey(
        CompanyContact,
        null=True,
        blank=True,
        verbose_name=_("contact"),
        on_delete=CASCADE,
    )
    image = ImageField(
        upload_to="joblistings/",
        null=True,
        blank=True,
        verbose_name=_("image"),
    )
    deadline = DateTimeField(null=True, blank=True, verbose_name=_("deadline"))
    from_grade = PositiveIntegerField(default=1, verbose_name=_("from grade"))
    to_grade = PositiveIntegerField(default=5, verbose_name=_("to grade"))
    towns = ManyToManyField(Town, blank=True, verbose_name=_("town"))
    url = URLField(blank=True, verbose_name=_("url"))
    is_active = BooleanField(verbose_name=_("active"), default=True)
    frontpage = BooleanField(_("Frontpage"), default=False)
    hide_contactinfo = BooleanField(_("Hide contact info"), default=False)
    slug = SlugField(editable=False, unique=True, max_length=150)
    video_url = URLField(null=True, blank=True, verbose_name=_("video"))
    is_summerjob_marathon = BooleanField(
        default=False, verbose_name=_("sommerjobbmaraton")
    )
    is_displayed = BooleanField(verbose_name=_("Show on website"), default=True)

    def __str__(self) -> str:
        return str(self.title)

    def get_absolute_url(self) -> str:
        return reverse("itdagene.career.view", args=[self.pk])

    def has_deadline_passed(self) -> bool:
        if self.deadline is None:
            return False
        return self.deadline < timezone.now()

    def get_towns(self) -> str:
        towns = [town.name for town in self.towns.all()]
        return ", ".join(towns)

    def get_classes(self) -> str:
        if self.from_grade != self.to_grade:
            return f"{self.from_grade}-{self.to_grade}"
        return self.to_year

    def save(self, *args, **kwargs):
        if not self.pk:
            slug_text = f"{self.company.name} {self.title} {now().year}"
            slug = slugify(slug_text)

            if Joblisting.objects.filter(slug=slug).exists():
                slug = slugify(slug_text + f" {now().month} {now().day}")

            self.slug = slug
        super(Joblisting, self).save(*args, **kwargs)

    class Meta:
        ordering = ("deadline", "pk")
        base_manager_name = "objects"

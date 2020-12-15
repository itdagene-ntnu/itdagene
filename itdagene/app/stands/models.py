from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from itdagene.app.company.models import Company
from itdagene.core.models import BaseModel


class DigitalStand(BaseModel):
    slug = models.SlugField(editable=True, unique=True, max_length=150, null=False)
    livestream = models.CharField(max_length=150, verbose_name=_("Livestream link"))
    qa = models.CharField(max_length=150, verbose_name=_("Q&A link"))
    chat = models.CharField(max_length=150, verbose_name=_("Chat link"))
    active = models.BooleanField(default=False, verbose_name=_("Active"))
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="digital_stand",
        verbose_name=_("Company"),
    )
    description = models.TextField(blank=True, verbose_name=_("description"))

    def get_absolute_url(self):
        return reverse("itdagene.stands.digitalstand.view", args=[self.pk])

    def __str__(self):
        return str(self.company.name + "-stand")

    def save(self, *args, **kwargs):
        if not self.pk:
            slug_text = f"{self.company.name}"
            slug = slugify(slug_text)

            if DigitalStand.objects.filter(slug=slug).exists():
                slug = slugify(slug_text + f" {now().year}")

            self.slug = slug
        super(DigitalStand, self).save(*args, **kwargs)

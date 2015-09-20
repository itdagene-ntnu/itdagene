from datetime import date

from django.db import models
from django.db.models import Q


class JoblistingManager(models.Manager):
    def active(self):
        return super(JoblistingManager, self).get_queryset().filter(
            (Q(deadline__gte=date.today()) | Q(deadline__isnull=True)),
            is_active=True
        )

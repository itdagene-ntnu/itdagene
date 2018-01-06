from django.db import models
from django.db.models import Q
from django.utils import timezone


class JoblistingManager(models.Manager):
    def active(self):
        return super(JoblistingManager, self).get_queryset().filter(
            (Q(deadline__gte=timezone.now()) | Q(deadline__isnull=True)), is_active=True
        )

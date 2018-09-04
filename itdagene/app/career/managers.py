from django.db import models
from django.db.models import Q
from django.db.models.aggregates import Sum
from django.utils import timezone


class JoblistingManager(models.Manager):
    def active(self):
        return super(JoblistingManager, self).get_queryset().filter(
            (Q(deadline__gte=timezone.now()) | Q(deadline__isnull=True)), is_active=True
        )

    def get_queryset(self):
        return super(JoblistingManager, self).get_queryset().filter(
            (Q(deadline__gte=timezone.now()) | Q(deadline__isnull=True)), is_active=True
        ).annotate(
            exclusivity=Sum("company__package__max"),
        ).order_by("exclusivity", "deadline", "id")

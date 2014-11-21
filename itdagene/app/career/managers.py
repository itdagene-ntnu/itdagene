from django.db import models
from datetime import date


class JoblistingManager(models.Manager):
    def active(self):
        return super(JoblistingManager, self).get_queryset().filter(deadline__gte=date.today())

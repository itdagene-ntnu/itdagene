from datetime import date

from django.db import models


class JoblistingManager(models.Manager):
    def active(self):
        return super(JoblistingManager, self).get_queryset().filter(deadline__gte=date.today(),
                                                                    is_active=True)

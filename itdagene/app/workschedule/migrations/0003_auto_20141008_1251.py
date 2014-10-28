# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workschedule', '0002_remove_worker_username'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='worker',
            options={'permissions': (('view_worker', 'Can see worker'),)},
        ),
    ]
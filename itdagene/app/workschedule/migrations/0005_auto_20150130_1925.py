# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workschedule', '0004_worker_preference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workschedule',
            name='description',
            field=models.TextField(verbose_name='Description', blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workschedule', '0003_auto_20141008_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='preference',
            field=models.PositiveIntegerField(default=2014, verbose_name='year'),
            preserve_default=False,
        ),
    ]

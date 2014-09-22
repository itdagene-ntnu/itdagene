# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0002_auto_20140923_0008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logitem',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2014, 9, 23, 0, 8, 28, 806380), verbose_name='dato'),
        ),
    ]

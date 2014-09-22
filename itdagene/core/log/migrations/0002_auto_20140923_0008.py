# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logitem',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2014, 9, 23, 0, 8, 18, 13001), verbose_name='dato'),
        ),
    ]

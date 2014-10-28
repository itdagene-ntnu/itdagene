# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0002_auto_20141013_1316'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stand',
            name='company_day1',
        ),
        migrations.RemoveField(
            model_name='stand',
            name='company_day2',
        ),
    ]

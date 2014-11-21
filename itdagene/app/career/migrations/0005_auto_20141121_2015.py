# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('career', '0004_auto_20141121_2014'),
    ]

    operations = [
        migrations.RenameField(
            model_name='joblisting',
            old_name='year',
            new_name='from_year',
        ),
    ]

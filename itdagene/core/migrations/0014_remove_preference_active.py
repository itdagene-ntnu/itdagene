# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_user_year'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preference',
            name='active',
        ),
    ]

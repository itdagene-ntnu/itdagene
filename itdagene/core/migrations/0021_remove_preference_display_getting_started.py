# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='preference',
            name='display_getting_started',
        ),
    ]

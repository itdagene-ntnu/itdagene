# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_auto_20140923_0007'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='user',
        ),
    ]

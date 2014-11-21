# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_auto_20141020_0000'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='mp',
        ),
        migrations.RemoveField(
            model_name='company',
            name='partner',
        ),
    ]

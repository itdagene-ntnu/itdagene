# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('career', '0002_auto_20140923_0007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joblisting',
            name='deadline',
            field=models.DateTimeField(null=True, verbose_name='deadline', blank=True),
        ),
    ]
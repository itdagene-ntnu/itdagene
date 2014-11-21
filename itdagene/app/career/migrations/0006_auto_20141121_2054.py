# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('career', '0005_auto_20141121_2015'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='joblisting',
            options={'ordering': ('-deadline',)},
        ),
        migrations.AddField(
            model_name='joblisting',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='active'),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('experiences', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experience',
            name='year',
            field=models.ForeignKey(verbose_name='Preference', to='core.Preference'),
        ),
    ]

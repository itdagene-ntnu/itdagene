# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20150922_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='type',
            field=models.PositiveIntegerField(verbose_name='type', choices=[(0, 'Course'), (1, 'Company presentation'), (2, 'Banquet'), (3, 'Summer internship marathon'), (4, 'Baloon drop'), (5, 'Competition')]),
            preserve_default=True,
        ),
    ]

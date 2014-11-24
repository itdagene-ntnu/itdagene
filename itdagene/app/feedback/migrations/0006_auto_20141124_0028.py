# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0005_evaluation_has_answers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='hash',
            field=models.CharField(unique=True, max_length=100, verbose_name='Hash'),
        ),
    ]

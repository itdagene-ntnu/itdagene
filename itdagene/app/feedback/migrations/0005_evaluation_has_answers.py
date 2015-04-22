# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('feedback', '0004_evaluation_hash'), ]

    operations = [migrations.AddField(
        model_name='evaluation',
        name='has_answers',
        field=models.BooleanField(default=False,
                                  verbose_name='has answers'),
        preserve_default=True, ), ]

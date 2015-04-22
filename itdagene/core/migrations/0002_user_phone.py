# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('core', '0001_initial'), ]

    operations = [migrations.AddField(
        model_name='user',
        name='phone',
        field=models.IntegerField(null=True,
                                  verbose_name='phone number',
                                  blank=True),
        preserve_default=True, ), ]

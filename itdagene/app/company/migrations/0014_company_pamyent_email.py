# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0013_auto_20160222_2053'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='pamyent_email',
            field=models.TextField(verbose_name='payment email', blank=True),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0012_auto_20160215_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companycontact',
            name='current',
            field=models.BooleanField(default=False, verbose_name='Current contact'),
            preserve_default=True,
        ),
    ]

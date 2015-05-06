# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import sorl.thumbnail.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0008_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=sorl.thumbnail.fields.ImageField(upload_to=b'company_logos/', null=True, verbose_name='logo', blank=True),
            preserve_default=True,
        ),
    ]

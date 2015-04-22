# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('core', '0010_auto_20140928_1748'), ]

    operations = [migrations.AddField(
        model_name='preference',
        name='development_mode',
        field=models.BooleanField(
            default=False,
            help_text=
            'This option puts the site in development mode. The public page will be disabled.',
            verbose_name='Development Mode'),
        preserve_default=True, ), ]

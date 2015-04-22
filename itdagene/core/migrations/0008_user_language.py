# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('core', '0007_auto_20140928_1537'), ]

    operations = [migrations.AddField(
        model_name='user',
        name='language',
        field=models.CharField(default=b'nb',
                               max_length=3,
                               choices=[('nb', 'Norsk'), ('en', 'English')]),
        preserve_default=True, ), ]

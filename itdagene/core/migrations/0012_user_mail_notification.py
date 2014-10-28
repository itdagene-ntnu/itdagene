# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_preference_development_mode'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mail_notification',
            field=models.BooleanField(default=True, verbose_name='Send mail notifications'),
            preserve_default=True,
        ),
    ]
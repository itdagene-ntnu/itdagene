# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_user_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='preference',
            name='display_getting_started',
            field=models.BooleanField(default=True, help_text='When this setting is enabled a getting started element is visible in the admin menu. This contains usefull information about how to use this site.', verbose_name='Display getting started in admin menu'),
            preserve_default=True,
        ),
    ]

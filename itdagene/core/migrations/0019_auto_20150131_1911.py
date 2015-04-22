# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_delete_userproxy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='year',
            field=models.PositiveIntegerField(default=2015, max_length=3000, blank=True, help_text='Year the user was active.', null=True, verbose_name='Active Year'),
        ),
    ]

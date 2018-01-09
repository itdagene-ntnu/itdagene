# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-12-29 16:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_merge_20171229_1651'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='year',
            field=models.PositiveIntegerField(
                blank=True, default=2017, help_text='Year the user was active.', null=True,
                verbose_name='Active Year'
            ),
        ),
    ]
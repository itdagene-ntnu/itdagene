# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_remove_company_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='company',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='reply_to',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='user',
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.AlterField(
            model_name='contract',
            name='timestamp',
            field=models.DateField(help_text='Signing date, not uploaded date', verbose_name='date'),
        ),
    ]

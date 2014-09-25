# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0002_auto_20140925_0223'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='restrictedmapping',
            name='address',
        ),
        migrations.AlterField(
            model_name='mailmapping',
            name='address',
            field=models.CharField(unique=True, max_length=100, verbose_name='Address'),
        ),
    ]

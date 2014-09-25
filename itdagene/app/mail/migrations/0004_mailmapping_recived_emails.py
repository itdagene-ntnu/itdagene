# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0003_auto_20140925_0235'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailmapping',
            name='recived_emails',
            field=models.IntegerField(default=0, max_length=9999999, verbose_name='Recived emails'),
            preserve_default=True,
        ),
    ]

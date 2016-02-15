# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0010_company_is_collaborator'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='companycontact',
            options={'ordering': ['-pk'], 'verbose_name': 'company contact', 'verbose_name_plural': 'company contacts'},
        ),
        migrations.AddField(
            model_name='companycontact',
            name='current',
            field=models.BooleanField(default=False, verbose_name='current contact'),
            preserve_default=True,
        ),
    ]

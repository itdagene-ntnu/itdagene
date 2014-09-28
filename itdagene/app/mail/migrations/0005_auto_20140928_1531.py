# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0004_mailmapping_recived_emails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailmapping',
            name='groups',
            field=models.ManyToManyField(related_name=b'group_mail_mappings', null=True, verbose_name='Groups', to=b'auth.Group', blank=True),
        ),
        migrations.AlterField(
            model_name='mailmapping',
            name='users',
            field=models.ManyToManyField(related_name=b'user_mail_mappings', null=True, verbose_name='Users', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]

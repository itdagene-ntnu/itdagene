# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notifications', '0007_auto_20150130_1925'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='read',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='user',
        ),
        migrations.AddField(
            model_name='notification',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name=b'users'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='subscription',
            unique_together=set([('content_type', 'object_id')]),
        ),
    ]

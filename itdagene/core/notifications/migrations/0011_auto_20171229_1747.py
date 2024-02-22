# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-12-29 16:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("notifications", "0010_auto_20161004_1437")]

    operations = [
        migrations.AlterField(
            model_name="subscription",
            name="subscribers",
            field=models.ManyToManyField(
                blank=True, related_name="subscriptions", to=settings.AUTH_USER_MODEL
            ),
        )
    ]

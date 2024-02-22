# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("core", "0022_auto_20160215_1141")]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="year",
            field=models.PositiveIntegerField(
                default=2017,
                max_length=3000,
                blank=True,
                help_text="Year the user was active.",
                null=True,
                verbose_name="Active Year",
            ),
            preserve_default=True,
        )
    ]

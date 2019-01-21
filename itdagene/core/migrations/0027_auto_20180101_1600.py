# Generated by Django 2.0 on 2018-01-01 15:00

import itdagene.core.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("core", "0026_auto_20171231_1831")]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="year",
            field=models.PositiveIntegerField(
                blank=True,
                default=itdagene.core.models.user_default_year,
                help_text="Year the user was active.",
                null=True,
                verbose_name="Active Year",
            ),
        )
    ]

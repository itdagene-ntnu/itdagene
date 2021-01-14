# Generated by Django 2.2.13 on 2020-12-17 12:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("stands", "0001_initial"),
        ("events", "0005_merge_20170405_1016"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="stand",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="stands.DigitalStand",
                verbose_name="Associated stand",
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="type",
            field=models.PositiveIntegerField(
                choices=[
                    (0, "Course"),
                    (1, "Company presentation"),
                    (2, "Banquet"),
                    (3, "Summer internship marathon"),
                    (4, "Baloon drop"),
                    (5, "Competition"),
                    (6, "Other"),
                ],
                verbose_name="type",
            ),
        ),
    ]

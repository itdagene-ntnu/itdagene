# Generated by Django 2.2.13 on 2020-12-16 14:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("company", "0022_auto_20180412_2018"),
    ]

    operations = [
        migrations.CreateModel(
            name="KeyInformation",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date_created", models.DateTimeField(editable=False)),
                ("date_saved", models.DateTimeField(editable=False)),
                (
                    "name",
                    models.CharField(max_length=20, verbose_name="information name"),
                ),
                ("value", models.CharField(max_length=20, verbose_name="value")),
                (
                    "company",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="key_information",
                        to="company.Company",
                        verbose_name="company",
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="keyinformation_creator",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "saved_by",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="keyinformation_saved_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
    ]

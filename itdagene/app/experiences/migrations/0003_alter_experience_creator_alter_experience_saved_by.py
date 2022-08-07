# Generated by Django 4.0.6 on 2022-08-07 15:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("experiences", "0002_auto_20161004_1437"),
    ]

    operations = [
        migrations.AlterField(
            model_name="experience",
            name="creator",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_creator",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="experience",
            name="saved_by",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="%(class)s_saved_by",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]

# Generated by Django 2.2.28 on 2024-04-26 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0034_auto_20220331_1113"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="linkedin",
            field=models.CharField(
                blank=True, max_length=255, null=True, verbose_name="LinkedIn"
            ),
        ),
    ]

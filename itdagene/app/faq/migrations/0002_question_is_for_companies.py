# Generated by Django 2.2.28 on 2024-09-10 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("faq", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="is_for_companies",
            field=models.BooleanField(default=False, verbose_name="For companies"),
        ),
    ]

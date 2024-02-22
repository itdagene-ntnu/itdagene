# Generated by Django 2.2.10 on 2020-09-14 08:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("career", "0020_auto_20200905_2352"),
    ]

    operations = [
        migrations.AddField(
            model_name="joblisting",
            name="is_summerjob_marathon",
            field=models.BooleanField(default=False, verbose_name="sommerjobbmaraton"),
        ),
        migrations.AddField(
            model_name="joblisting",
            name="video_url",
            field=models.URLField(blank=True, null=True, verbose_name="video"),
        ),
    ]

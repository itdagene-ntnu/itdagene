# Generated by Django 2.0 on 2017-12-31 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("core", "0025_auto_20171229_1747")]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="last_name",
            field=models.CharField(
                blank=True, max_length=150, verbose_name="last name"
            ),
        )
    ]

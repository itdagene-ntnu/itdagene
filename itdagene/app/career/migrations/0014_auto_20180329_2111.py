# Generated by Django 2.0.3 on 2018-03-29 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("career", "0013_auto_20171231_1831")]

    operations = [
        migrations.AlterModelOptions(
            name="joblisting",
            options={
                "base_manager_name": "objects",
                "ordering": ("deadline", )
            },
        )
    ]

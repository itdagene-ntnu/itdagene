# Generated by Django 2.1.2 on 2018-10-08 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workschedule', '0006_auto_20161004_1437'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='worker',
            options={},
        ),
        migrations.AlterModelOptions(
            name='workschedule',
            options={
                'verbose_name': 'work schedule',
                'verbose_name_plural': 'work schedules'
            },
        ),
    ]

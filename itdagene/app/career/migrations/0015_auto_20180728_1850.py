# Generated by Django 2.0.6 on 2018-07-28 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('career', '0014_auto_20180329_2111'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='joblisting',
            options={'base_manager_name': 'objects', 'ordering': ('deadline', 'pk')},
        ),
    ]

# Generated by Django 2.0 on 2018-01-06 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_auto_20180101_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='language',
            field=models.CharField(
                choices=[('nb', 'Norsk')], default='nb', max_length=3, verbose_name='Language'
            ),
        ),
    ]

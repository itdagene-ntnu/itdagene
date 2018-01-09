# Generated by Django 1.10.2 on 2016-10-04 12:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20150922_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='type',
            field=models.PositiveIntegerField(
                choices=[
                    (0, 'Course'), (1, 'Company presentation'), (2, 'Banquet'),
                    (3, 'Summer internship marathon'), (4, 'Baloon drop'), (5, 'Competition')
                ], verbose_name='type'
            ),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='e-mail address'),
        ),
    ]
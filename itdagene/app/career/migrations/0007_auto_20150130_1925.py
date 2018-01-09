from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('career', '0006_auto_20141121_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joblisting',
            name='description',
            field=models.TextField(verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='joblisting',
            name='from_year',
            field=models.PositiveIntegerField(default=1, verbose_name='from year'),
        ),
        migrations.AlterField(
            model_name='joblisting',
            name='to_year',
            field=models.PositiveIntegerField(default=5, verbose_name='to year'),
        ),
        migrations.AlterField(
            model_name='joblisting',
            name='type',
            field=models.CharField(
                max_length=20, verbose_name='type',
                choices=[(b'si', 'Summer internship'), (b'pp', 'Permanent position')]
            ),
        ),
    ]

from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0005_auto_20141121_2122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='phone',
            field=models.CharField(max_length=20, null=True, verbose_name='Phone', blank=True),
        ),
        migrations.AlterField(
            model_name='contract',
            name='file',
            field=models.FileField(upload_to='contracts/', verbose_name='file'),
        ),
    ]

# Generated by Django 2.0.3 on 2018-04-12 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0021_auto_20180412_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo_vector',
            field=models.FileField(
                blank=True, null=True, upload_to='company_logos/', verbose_name='logo_vector'
            ),
        ),
    ]

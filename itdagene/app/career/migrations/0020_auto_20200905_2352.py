# Generated by Django 2.2.10 on 2020-09-05 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('career', '0019_fix_slugs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joblisting',
            name='type',
            field=models.CharField(choices=[('si', 'Summer internship'), ('pp', 'Permanent position'), ('ot', 'Other')], max_length=20, verbose_name='type'),
        ),
    ]

from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0011_auto_20160215_1128'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='companycontact',
            options={
                'ordering': ['-current', '-pk'],
                'verbose_name': 'company contact',
                'verbose_name_plural': 'company contacts'
            },
        ),
        migrations.AlterField(
            model_name='companycontact',
            name='current',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]

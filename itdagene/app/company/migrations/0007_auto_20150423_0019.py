from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0006_auto_20150130_1925'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={
                'ordering': ('name', ),
                'verbose_name': 'company',
                'verbose_name_plural': 'companies'
            },
        ),
    ]

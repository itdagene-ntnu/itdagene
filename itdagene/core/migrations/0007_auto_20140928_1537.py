from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('core', '0006_auto_20140928_1535'), ]

    operations = [migrations.AlterModelOptions(
        name='user',
        options={
            'verbose_name': 'user',
            'verbose_name_plural': 'users',
            'permissions': (('send_welcome_email', 'Can send welcome emails'), )
        }, ), ]

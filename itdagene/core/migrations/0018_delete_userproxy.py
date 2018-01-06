from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('core', '0017_remove_user_mail_prefix'), ]

    operations = [migrations.DeleteModel(name='UserProxy', ), ]

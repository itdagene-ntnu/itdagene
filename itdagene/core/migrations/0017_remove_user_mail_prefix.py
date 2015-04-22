# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('core', '0016_auto_20141007_2055'), ]

    operations = [migrations.RemoveField(model_name='user',
                                         name='mail_prefix', ), ]

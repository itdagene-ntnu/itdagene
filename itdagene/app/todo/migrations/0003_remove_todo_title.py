# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('todo', '0002_auto_20140930_1404'), ]

    operations = [migrations.RemoveField(model_name='todo', name='title', ), ]

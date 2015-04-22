# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL),
                    ('comments', '0001_initial'), ]

    operations = [migrations.AddField(
        model_name='comment',
        name='user',
        field=models.ForeignKey(verbose_name='user',
                                to=settings.AUTH_USER_MODEL),
        preserve_default=True, ), ]

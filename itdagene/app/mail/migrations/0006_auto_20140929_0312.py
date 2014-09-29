# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mail', '0005_auto_20140928_1531'),
    ]

    operations = [
        migrations.AddField(
            model_name='mailmapping',
            name='creator',
            field=models.ForeignKey(related_name=b'mailmapping_creator', default=0, editable=False, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mailmapping',
            name='date_created',
            field=models.DateTimeField(default=datetime.date(2014, 9, 29), editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mailmapping',
            name='date_saved',
            field=models.DateTimeField(default=datetime.date(2014, 9, 29), editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='mailmapping',
            name='saved_by',
            field=models.ForeignKey(related_name=b'mailmapping_saved_by', default=0, editable=False, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]

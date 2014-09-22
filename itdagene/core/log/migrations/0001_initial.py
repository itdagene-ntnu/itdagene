# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('priority', models.PositiveIntegerField(default=1, verbose_name='prioritet', choices=[(0, b'Low'), (1, b'Medium'), (2, b'High'), (3, b'Very High. Will send email to administrators')])),
                ('timestamp', models.DateTimeField(default=datetime.datetime(2014, 9, 23, 0, 7, 7, 195155), verbose_name='dato')),
                ('action', models.CharField(max_length=16, verbose_name='handling')),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(verbose_name='bruker', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

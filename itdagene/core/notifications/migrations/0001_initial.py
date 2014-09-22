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
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('priority', models.PositiveIntegerField(default=1, verbose_name='prioritet', choices=[(0, b'Low'), (1, b'Medium'), (2, b'High')])),
                ('date', models.DateTimeField(default=datetime.datetime(2014, 9, 23, 0, 7, 7, 220940), verbose_name='dato')),
                ('message', models.TextField(verbose_name='melding')),
                ('object_id', models.PositiveIntegerField()),
                ('send_mail', models.BooleanField(default=True, verbose_name='send epost')),
                ('sent_mail', models.BooleanField(default=False, verbose_name='sendt epost')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(verbose_name='bruker', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('subscribers', models.ManyToManyField(related_name=b'subscriptions', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

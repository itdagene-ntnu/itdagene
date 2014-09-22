# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('company', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomRegistration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(editable=False)),
                ('date_saved', models.DateTimeField(editable=False)),
                ('room_nr', models.CharField(max_length=10, verbose_name='room number')),
                ('date', models.DateField(verbose_name='date')),
                ('time_start', models.TimeField(verbose_name='start time')),
                ('time_end', models.TimeField(verbose_name='end time')),
                ('confirmed', models.BooleanField(default=False, verbose_name='confirmed')),
                ('receipt', models.TextField(verbose_name='receipt', blank=True)),
                ('company', models.ForeignKey(verbose_name='company', blank=True, to='company.Company', null=True)),
                ('creator', models.ForeignKey(related_name=b'roomregistration_creator', editable=False, to=settings.AUTH_USER_MODEL)),
                ('saved_by', models.ForeignKey(related_name=b'roomregistration_saved_by', editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]

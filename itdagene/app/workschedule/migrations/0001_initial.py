# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL),
                    ]

    operations = [migrations.CreateModel(
        name='Worker',
        fields=[('id', models.AutoField(verbose_name='ID',
                                        serialize=False,
                                        auto_created=True,
                                        primary_key=True)),
                ('date_created', models.DateTimeField(editable=False)),
                ('date_saved', models.DateTimeField(editable=False)),
                ('username', models.CharField(max_length=20,
                                              verbose_name='username',
                                              blank=True)),
                ('name', models.CharField(max_length=100,
                                          verbose_name='name')),
                ('phone', models.IntegerField(default=0,
                                              verbose_name='phone number')),
                ('t_shirt_size', models.IntegerField(
                    default=0,
                    verbose_name='t-shirt size',
                    choices=[(1, b'XS'), (2, b'S'), (3, b'M'), (4, b'L'), (
                        5, b'XL'), (6, b'XXL'), (7, b'XXXL'), (8, b'XXXXL')])),
                ('email', models.EmailField(max_length=75,
                                            verbose_name='email',
                                            blank=True)),
                ('creator', models.ForeignKey(related_name=b'worker_creator',
                                              editable=False,
                                              to=settings.AUTH_USER_MODEL)),
                ('saved_by', models.ForeignKey(related_name=b'worker_saved_by',
                                               editable=False,
                                               to=settings.AUTH_USER_MODEL)), ],
        options={'abstract': False, },
        bases=(models.Model, ), ),
                  migrations.CreateModel(
                      name='WorkerInSchedule',
                      fields=
                      [('id', models.AutoField(verbose_name='ID',
                                               serialize=False,
                                               auto_created=True,
                                               primary_key=True)),
                       ('date_created', models.DateTimeField(editable=False)),
                       ('date_saved', models.DateTimeField(editable=False)),
                       ('has_met', models.BooleanField(default=False,
                                                       verbose_name='has met')),
                       ('creator', models.ForeignKey(
                           related_name=b'workerinschedule_creator',
                           editable=False,
                           to=settings.AUTH_USER_MODEL)),
                       ('saved_by', models.ForeignKey(
                           related_name=b'workerinschedule_saved_by',
                           editable=False,
                           to=settings.AUTH_USER_MODEL)), ],
                      options={'abstract': False, },
                      bases=(models.Model, ), ),
                  migrations.CreateModel(
                      name='WorkSchedule',
                      fields=
                      [('id', models.AutoField(verbose_name='ID',
                                               serialize=False,
                                               auto_created=True,
                                               primary_key=True)),
                       ('date_created', models.DateTimeField(editable=False)),
                       ('date_saved', models.DateTimeField(editable=False)),
                       ('title', models.CharField(max_length=80,
                                                  verbose_name='title')),
                       ('date', models.DateField(verbose_name='date')),
                       ('start_time', models.TimeField(verbose_name='start time')),
                       ('end_time', models.TimeField(verbose_name='end time')),
                       ('description', models.TextField(blank=True)),
                       ('creator',
                        models.ForeignKey(related_name=b'workschedule_creator',
                                          editable=False,
                                          to=settings.AUTH_USER_MODEL)),
                       ('saved_by', models.ForeignKey(
                           related_name=b'workschedule_saved_by',
                           editable=False,
                           to=settings.AUTH_USER_MODEL)), ],
                      options={
                          'verbose_name': 'work schedule',
                          'verbose_name_plural': 'work schedules',
                          'permissions': (('view_workschedule',
                                           'Can see workschedule'), ),
                      },
                      bases=(models.Model, ), ),
                  migrations.AddField(
                      model_name='workerinschedule',
                      name='schedule',
                      field=models.ForeignKey(related_name=b'workers_in_schedule',
                                              verbose_name='schedule',
                                              to='workschedule.WorkSchedule'),
                      preserve_default=True, ),
                  migrations.AddField(
                      model_name='workerinschedule',
                      name='worker',
                      field=models.ForeignKey(related_name=b'in_schedules',
                                              verbose_name='worker',
                                              to='workschedule.Worker'),
                      preserve_default=True, ), ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Stand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(editable=False)),
                ('date_saved', models.DateTimeField(editable=False)),
                ('section', models.CharField(max_length=1)),
                ('stand_nr', models.PositiveIntegerField()),
                ('lat', models.DecimalField(null=True, max_digits=8, decimal_places=6, blank=True)),
                ('lon', models.DecimalField(null=True, max_digits=8, decimal_places=6, blank=True)),
                ('company_day1', models.ForeignKey(related_name=b'stand_day1', blank=True, to='company.Company', null=True)),
                ('company_day2', models.ForeignKey(related_name=b'stand_day2', blank=True, to='company.Company', null=True)),
                ('creator', models.ForeignKey(related_name=b'stand_creator', editable=False, to=settings.AUTH_USER_MODEL)),
                ('saved_by', models.ForeignKey(related_name=b'stand_saved_by', editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]

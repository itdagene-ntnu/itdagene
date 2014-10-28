# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_auto_20140923_0007'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('venue', '0003_auto_20141013_1326'),
    ]

    operations = [
        migrations.CreateModel(
            name='StandCompany',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(editable=False)),
                ('date_saved', models.DateTimeField(editable=False)),
                ('date', models.DateField(verbose_name='date')),
                ('company', models.ForeignKey(related_name=b'stands', verbose_name='company', to='company.Company')),
                ('creator', models.ForeignKey(related_name=b'standcompany_creator', editable=False, to=settings.AUTH_USER_MODEL)),
                ('saved_by', models.ForeignKey(related_name=b'standcompany_saved_by', editable=False, to=settings.AUTH_USER_MODEL)),
                ('stand', models.ForeignKey(related_name=b'stand_companies', verbose_name='stand', to='venue.Stand')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='standcompany',
            unique_together=set([('date', 'stand'), ('date', 'company')]),
        ),
    ]

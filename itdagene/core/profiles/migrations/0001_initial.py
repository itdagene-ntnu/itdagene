# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BoardPosition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(editable=False)),
                ('date_saved', models.DateTimeField(editable=False)),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('email', models.EmailField(default=b'', max_length=75, null=True, verbose_name='email', blank=True)),
                ('creator', models.ForeignKey(related_name=b'boardposition_creator', editable=False, to=settings.AUTH_USER_MODEL)),
                ('saved_by', models.ForeignKey(related_name=b'boardposition_saved_by', editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Boardposition',
                'verbose_name_plural': 'Boardpositions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(editable=False)),
                ('date_saved', models.DateTimeField(editable=False)),
                ('type', models.CharField(default=b'u', max_length=1, verbose_name='type', choices=[(b'b', 'Board member'), (b'c', 'Company profile'), (b'w', 'Workers'), (b'u', 'Unknown')])),
                ('year', models.IntegerField(help_text='The year this person arranged itDAGENE', null=True, verbose_name='year', blank=True)),
                ('phone', models.IntegerField(null=True, verbose_name='phone number', blank=True)),
                ('language', models.CharField(default=b'nb', max_length=3, choices=[('nb', 'Norsk'), ('en', 'English')])),
                ('photo', models.ImageField(null=True, upload_to=b'photos/profiles/', blank=True)),
                ('mail_notification', models.BooleanField(default=True, help_text='If you uncheck this the website will not send email you notifications.', verbose_name='mail notification')),
                ('creator', models.ForeignKey(related_name=b'profile_creator', editable=False, to=settings.AUTH_USER_MODEL)),
                ('position', models.ForeignKey(verbose_name='position', blank=True, to='profiles.BoardPosition', null=True)),
                ('saved_by', models.ForeignKey(related_name=b'profile_saved_by', editable=False, to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(related_name=b'profile', verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
            bases=(models.Model,),
        ),
    ]

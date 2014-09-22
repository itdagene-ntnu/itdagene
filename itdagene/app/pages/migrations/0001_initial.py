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
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_created', models.DateTimeField(editable=False)),
                ('date_saved', models.DateTimeField(editable=False)),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('slug', models.SlugField(max_length=100, verbose_name='slug')),
                ('content', models.TextField(verbose_name='content')),
                ('language', models.CharField(default=b'nb', max_length=3, choices=[('nb', 'Norsk'), ('en', 'English')])),
                ('active', models.BooleanField(default=False, verbose_name='active')),
                ('need_auth', models.BooleanField(default=False, verbose_name='need authentication')),
                ('menu', models.BooleanField(default=False, verbose_name='should be in menu')),
                ('creator', models.ForeignKey(related_name=b'page_creator', editable=False, to=settings.AUTH_USER_MODEL)),
                ('saved_by', models.ForeignKey(related_name=b'page_saved_by', editable=False, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
            },
            bases=(models.Model,),
        ),
    ]

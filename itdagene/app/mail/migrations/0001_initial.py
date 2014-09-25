# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MailMapping',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=100, verbose_name='Address')),
                ('groups', models.ManyToManyField(related_name=b'mail_mappings', verbose_name='Groups', to='auth.Group', blank=True)),
                ('users', models.ManyToManyField(related_name=b'mail_mappings', verbose_name='Users', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'permissions': (('mail_access', 'Can access mail app'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RestrictedMapping',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=100, verbose_name='Address')),
                ('token', models.CharField(max_length=70, verbose_name='Token')),
                ('from_address', models.EmailField(max_length=75, null=True, verbose_name='From address')),
                ('timeout', models.DateTimeField(auto_now=True, verbose_name='Timeout')),
                ('groups', models.ManyToManyField(to='auth.Group', verbose_name='Groups', blank=True)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Users', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

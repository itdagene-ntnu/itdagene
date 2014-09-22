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
        migrations.AddField(
            model_name='package',
            name='creator',
            field=models.ForeignKey(related_name=b'package_creator', editable=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='package',
            name='saved_by',
            field=models.ForeignKey(related_name=b'package_saved_by', editable=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contract',
            name='company',
            field=models.ForeignKey(related_name=b'contracts', verbose_name='company', to='company.Company'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contract',
            name='creator',
            field=models.ForeignKey(related_name=b'contract_creator', editable=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contract',
            name='saved_by',
            field=models.ForeignKey(related_name=b'contract_saved_by', editable=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companycontact',
            name='company',
            field=models.ForeignKey(related_name=b'company_contacts', verbose_name='company', to='company.Company'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companycontact',
            name='creator',
            field=models.ForeignKey(related_name=b'companycontact_creator', editable=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companycontact',
            name='saved_by',
            field=models.ForeignKey(related_name=b'companycontact_saved_by', editable=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='contact',
            field=models.ForeignKey(related_name=b'contact_for', verbose_name='itDAGENE contact', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='creator',
            field=models.ForeignKey(related_name=b'company_creator', editable=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='package',
            field=models.ForeignKey(related_name=b'companies', verbose_name='package', blank=True, to='company.Package', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='saved_by',
            field=models.ForeignKey(related_name=b'company_saved_by', editable=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='user',
            field=models.ForeignKey(related_name=b'company', verbose_name='user', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='waiting_for_package',
            field=models.ManyToManyField(related_name=b'waiting_list', null=True, verbose_name='waiting for package', to='company.Package', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='company',
            field=models.ForeignKey(verbose_name='company', to='company.Company'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='reply_to',
            field=models.ForeignKey(related_name=b'replies', verbose_name='reply to', blank=True, to='company.Comment', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(related_name=b'company_comment', verbose_name='user', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='callteam',
            name='creator',
            field=models.ForeignKey(related_name=b'callteam_creator', editable=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='callteam',
            name='saved_by',
            field=models.ForeignKey(related_name=b'callteam_saved_by', editable=False, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='callteam',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='users'),
            preserve_default=True,
        ),
    ]

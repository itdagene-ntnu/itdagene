from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='creator',
            field=models.ForeignKey(
                related_name='package_creator', editable=False, on_delete=models.CASCADE,
                to=settings.AUTH_USER_MODEL
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='package',
            name='saved_by',
            field=models.ForeignKey(
                related_name='package_saved_by', on_delete=models.CASCADE, editable=False,
                to=settings.AUTH_USER_MODEL
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contract',
            name='company',
            field=models.ForeignKey(
                related_name='contracts', on_delete=models.CASCADE, verbose_name='company',
                to='company.Company'
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contract',
            name='creator',
            field=models.ForeignKey(
                related_name='contract_creator', on_delete=models.CASCADE, editable=False,
                to=settings.AUTH_USER_MODEL
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contract',
            name='saved_by',
            field=models.ForeignKey(
                related_name='contract_saved_by',
                editable=False,
                to=settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companycontact',
            name='company',
            field=models.ForeignKey(
                related_name='company_contacts',
                verbose_name='company',
                to='company.Company',
                on_delete=models.CASCADE,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companycontact',
            name='creator',
            field=models.ForeignKey(
                related_name='companycontact_creator',
                editable=False,
                to=settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='companycontact',
            name='saved_by',
            field=models.ForeignKey(
                related_name='companycontact_saved_by',
                editable=False,
                to=settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='contact',
            field=models.ForeignKey(
                related_name='contact_for',
                verbose_name='itDAGENE contact',
                blank=True,
                to=settings.AUTH_USER_MODEL,
                null=True,
                on_delete=models.SET_NULL,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='creator',
            field=models.ForeignKey(
                related_name='company_creator',
                editable=False,
                to=settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='package',
            field=models.ForeignKey(
                related_name='companies',
                verbose_name='package',
                blank=True,
                to='company.Package',
                null=True,
                on_delete=models.SET_NULL,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='saved_by',
            field=models.ForeignKey(
                related_name='company_saved_by',
                editable=False,
                to=settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='user',
            field=models.ForeignKey(
                related_name='company',
                verbose_name='user',
                blank=True,
                to=settings.AUTH_USER_MODEL,
                null=True,
                on_delete=models.SET_NULL,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='company',
            name='waiting_for_package',
            field=models.ManyToManyField(
                related_name='waiting_list', null=True, verbose_name='waiting for package',
                to='company.Package', blank=True
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='company',
            field=models.ForeignKey(
                verbose_name='company',
                to='company.Company',
                on_delete=models.CASCADE,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='reply_to',
            field=models.ForeignKey(
                related_name='replies', verbose_name='reply to', blank=True, to='company.Comment',
                on_delete=models.SET_NULL, null=True
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(
                related_name='company_comment',
                verbose_name='user',
                to=settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='callteam',
            name='creator',
            field=models.ForeignKey(
                related_name='callteam_creator',
                editable=False,
                to=settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='callteam',
            name='saved_by',
            field=models.ForeignKey(
                related_name='callteam_saved_by',
                editable=False,
                to=settings.AUTH_USER_MODEL,
                on_delete=models.CASCADE,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='callteam',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='users'),
            preserve_default=True,
        ),
    ]

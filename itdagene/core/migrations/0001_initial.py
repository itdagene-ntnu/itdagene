from __future__ import unicode_literals

import django.core.validators
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True, primary_key=True
                    )
                ),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                (
                    'last_login',
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name='last login'
                    )
                ),
                (
                    'is_superuser',
                    models.BooleanField(
                        default=False, help_text=
                        'Designates that this user has all permissions without explicitly assigning them.',
                        verbose_name='superuser status'
                    )
                ),
                (
                    'username',
                    models.CharField(
                        help_text=
                        'Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.',
                        unique=True, max_length=30, verbose_name='username', validators=[
                            django.core.validators.RegexValidator(
                                '^[\\w.@+-]+$', 'Enter a valid username.', 'invalid'
                            )
                        ]
                    )
                ),
                (
                    'first_name',
                    models.CharField(max_length=30, verbose_name='first name', blank=True)
                ),
                (
                    'last_name',
                    models.CharField(max_length=30, verbose_name='last name', blank=True)
                ),
                (
                    'email',
                    models.EmailField(max_length=75, verbose_name='email address', blank=True)
                ),
                (
                    'is_staff',
                    models.BooleanField(
                        default=False,
                        help_text='Designates whether the user can log into this admin site.',
                        verbose_name='staff status'
                    )
                ),
                (
                    'is_active',
                    models.BooleanField(
                        default=True, help_text=
                        'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.',
                        verbose_name='active'
                    )
                ),
                (
                    'date_joined',
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name='date joined'
                    )
                ),
                (
                    'groups',
                    models.ManyToManyField(
                        related_query_name='user', related_name='user_set', to='auth.Group',
                        blank=True, help_text=
                        'The groups this user belongs to. A user will get all permissions granted to each of his/her group.',
                        verbose_name='groups'
                    )
                ),
                (
                    'user_permissions',
                    models.ManyToManyField(
                        related_query_name='user', related_name='user_set', to='auth.Permission',
                        blank=True, help_text='Specific permissions for this user.',
                        verbose_name='user permissions'
                    )
                ),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='Preference',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True, primary_key=True
                    )
                ),
                ('date_created', models.DateTimeField(editable=False)),
                ('date_saved', models.DateTimeField(editable=False)),
                ('active', models.BooleanField(default=False, verbose_name='active')),
                ('year', models.IntegerField(null=True, verbose_name='year', blank=True)),
                ('start_date', models.DateField(verbose_name='start date')),
                ('end_date', models.DateField(verbose_name='end date')),
                (
                    'nr_of_stands',
                    models.PositiveIntegerField(
                        default=30, help_text='This is for each day, not the sum of each day',
                        verbose_name='number of stands'
                    )
                ),
                ('view_sp', models.BooleanField(default=False, verbose_name='view partners')),
                (
                    'creator',
                    models.ForeignKey(
                        related_name='preference_creator', on_delete=models.CASCADE, editable=False,
                        to=settings.AUTH_USER_MODEL
                    )
                ),
                (
                    'saved_by',
                    models.ForeignKey(
                        related_name='preference_saved_by', on_delete=models.CASCADE,
                        editable=False, to=settings.AUTH_USER_MODEL
                    )
                ),
            ],
            options={
                'verbose_name': 'Preference',
                'verbose_name_plural': 'Preferences',
            },
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='UserProxy',
            fields=[],
            options={
                'proxy': True,
            },
            bases=('core.user', ),
        ),
    ]

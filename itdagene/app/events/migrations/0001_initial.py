from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True, primary_key=True
                    )
                ),
                ('date_created', models.DateTimeField(editable=False)),
                ('date_saved', models.DateTimeField(editable=False)),
                ('title', models.CharField(max_length=80, verbose_name='title')),
                ('date', models.DateField(verbose_name='date')),
                ('time_start', models.TimeField(verbose_name='start time')),
                ('time_end', models.TimeField(verbose_name='end time')),
                ('description', models.TextField(verbose_name='description')),
                (
                    'type',
                    models.PositiveIntegerField(
                        verbose_name='type',
                        choices=[(0, 'Course'), (1, 'Company presentation'), (2, 'Banquet')]
                    )
                ),
                ('location', models.CharField(max_length=30, verbose_name='location')),
                ('is_internal', models.BooleanField(default=False, verbose_name='internal event')),
                ('uses_tickets', models.BooleanField(default=False, verbose_name='uses tickets')),
                (
                    'max_participants',
                    models.PositiveIntegerField(
                        null=True, verbose_name='max nr of participants', blank=True
                    )
                ),
                (
                    'company',
                    models.ForeignKey(
                        verbose_name='hosting company', blank=True, on_delete=models.SET_NULL,
                        to='company.Company', null=True
                    )
                ),
                (
                    'creator',
                    models.ForeignKey(
                        related_name='event_creator', editable=False, on_delete=models.CASCADE,
                        to=settings.AUTH_USER_MODEL
                    )
                ),
                (
                    'saved_by',
                    models.ForeignKey(
                        related_name='event_saved_by', editable=False, on_delete=models.CASCADE,
                        to=settings.AUTH_USER_MODEL
                    )
                ),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, ),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                (
                    'id',
                    models.AutoField(
                        verbose_name='ID', serialize=False, auto_created=True, primary_key=True
                    )
                ),
                ('date_created', models.DateTimeField(editable=False)),
                ('date_saved', models.DateTimeField(editable=False)),
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
                    models.EmailField(max_length=75, verbose_name='e-mail address', blank=True)
                ),
                (
                    'company',
                    models.ForeignKey(
                        related_name='tickets', verbose_name='company', blank=True,
                        on_delete=models.SET_NULL, to='company.Company', null=True
                    )
                ),
                (
                    'creator',
                    models.ForeignKey(
                        related_name='ticket_creator',
                        editable=False,
                        to=settings.AUTH_USER_MODEL,
                        on_delete=models.CASCADE,
                    )
                ),
                (
                    'event',
                    models.ForeignKey(
                        related_name='tickets',
                        verbose_name='event',
                        to='events.Event',
                        on_delete=models.CASCADE,
                    )
                ),
                (
                    'saved_by',
                    models.ForeignKey(
                        related_name='ticket_saved_by',
                        editable=False,
                        to=settings.AUTH_USER_MODEL,
                        on_delete=models.CASCADE,
                    )
                ),
                (
                    'user',
                    models.ForeignKey(
                        blank=True, to=settings.AUTH_USER_MODEL,
                        help_text='If the person does not have a user, use the fields below.',
                        on_delete=models.SET_NULL, null=True, verbose_name='user'
                    )
                ),
            ],
            options={
                'ordering': ('company__name', ),
            },
            bases=(models.Model, ),
        ),
    ]

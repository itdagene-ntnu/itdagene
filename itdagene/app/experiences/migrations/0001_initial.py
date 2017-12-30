from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_preference_active'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Experience',
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
                    'position',
                    models.PositiveIntegerField(
                        default=8, verbose_name='Position', choices=[
                            (0, b'Leder'), (1, b'Nestleder'), (2, b'Okonomi'),
                            (3, b'Bedriftskontaktansvarlig'), (4,
                                                               b'Logistikk'), (5, b'Markedsforing'),
                            (6, b'Web'), (7, b'Bankett'), (8, b'Bedriftskontakt')
                        ]
                    )
                ),
                ('last_updated', models.DateField(auto_now=True)),
                ('text', models.TextField(null=True, verbose_name='Experiences', blank=True)),
                (
                    'creator',
                    models.ForeignKey(
                        related_name=b'experience_creator', editable=False,
                        on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL
                    )
                ),
                (
                    'saved_by',
                    models.ForeignKey(
                        related_name=b'experience_saved_by', editable=False,
                        on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL
                    )
                ),
                (
                    'year',
                    models.ForeignKey(
                        verbose_name='Preference',
                        to='core.Preference',
                        on_delete=models.CASCADE,
                    )
                ),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, ),
        ),
    ]

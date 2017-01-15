from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Joblisting',
            fields=[('id', models.AutoField(verbose_name='ID',
                                            serialize=False,
                                            auto_created=True,
                                            primary_key=True)),
                    ('date_created', models.DateTimeField(editable=False)),
                    ('date_saved', models.DateTimeField(editable=False)),
                    ('title', models.CharField(max_length=160,
                                               verbose_name='title')),
                    ('type',
                     models.CharField(max_length=20,
                                      verbose_name='type',
                                      choices=[(b'si', 'Summer internship'),
                                               (b'pp', 'Permanent position'),
                                               (b'bi', 'Bad import')])),
                    ('description', models.TextField()),
                    ('image', models.ImageField(upload_to=b'joblistings/',
                                                null=True,
                                                verbose_name='image',
                                                blank=True)),
                    ('deadline', models.DateField(null=True,
                                                  verbose_name='deadline',
                                                  blank=True)),
                    ('from_year', models.PositiveIntegerField(default=1)),
                    ('to_year', models.PositiveIntegerField(default=5)),
                    ('url', models.URLField(verbose_name='url',
                                            blank=True)), ],
            options={'abstract': False, },
            bases=(models.Model, ), ),
        migrations.CreateModel(
            name='Town',
            fields=[('id', models.AutoField(verbose_name='ID',
                                            serialize=False,
                                            auto_created=True,
                                            primary_key=True)),
                    ('date_created', models.DateTimeField(editable=False)),
                    ('date_saved', models.DateTimeField(editable=False)),
                    ('name', models.CharField(max_length=100,
                                              verbose_name='name')), ],
            options={'abstract': False, },
            bases=(models.Model, ), ),
    ]

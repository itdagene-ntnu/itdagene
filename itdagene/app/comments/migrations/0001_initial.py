from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('contenttypes', '0001_initial'), ]

    operations = [migrations.CreateModel(
        name='Comment',
        fields=[('id', models.AutoField(verbose_name='ID',
                                        serialize=False,
                                        auto_created=True,
                                        primary_key=True)),
                ('comment', models.TextField(verbose_name='comment')),
                ('date', models.DateTimeField(verbose_name='date')),
                ('object_id', models.PositiveIntegerField(null=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType',
                                                   null=True)),
                ('reply_to', models.ForeignKey(related_name=b'replies',
                                               blank=True,
                                               to='comments.Comment',
                                               null=True)), ],
        options={},
        bases=(models.Model, ), ), ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('company', '0002_auto_20140923_0007'),
                    ('core', '0012_user_mail_notification'),
                    ('feedback', '0001_initial'), ]

    operations = [
        migrations.AlterUniqueTogether(name='evaluationhash',
                                       unique_together=None, ),
        migrations.RemoveField(model_name='evaluationhash',
                               name='company', ),
        migrations.RemoveField(model_name='evaluationhash',
                               name='preference', ),
        migrations.RemoveField(model_name='evaluation',
                               name='hash', ),
        migrations.DeleteModel(name='EvaluationHash', ),
        migrations.AddField(model_name='evaluation',
                            name='company',
                            field=models.ForeignKey(default=None,
                                                    verbose_name=b'Company',
                                                    to='company.Company'),
                            preserve_default=False, ),
        migrations.AddField(model_name='evaluation',
                            name='preference',
                            field=models.ForeignKey(default=0,
                                                    verbose_name=b'Preference',
                                                    to='core.Preference'),
                            preserve_default=False, ),
        migrations.AlterField(
            model_name='issue',
            name='app',
            field=models.CharField(max_length=50,
                                   verbose_name='app',
                                   choices=[(b'all', 'All'), (b'admin', 'Admin'
                                   ), (b'company', 'BDB'), (b'career', 'Career'
                  ), (b'core', 'Core'), (b'documents', 'Documents'), (
                      b'events', 'Events'
                  ), (b'feedback', 'Feedback'), (b'frontpage', 'Frontpage'), (
                      b'logistics', 'Logistics'
                  ), (b'mail', 'Mail'), (b'meetings', 'Meetings'), (
                      b'news', 'News'), (b'notifications', 'Notifications'), (
                          b'pages', 'Pages'), (b'profiles', 'Profiles'), (
                              b'todo', 'Todo'), (b'venue', 'Venue'), (
                                  b'workschedule', 'Workschedule')]), ),
    ]

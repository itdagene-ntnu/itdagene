from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0002_auto_20141001_0202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evaluation',
            name='visitors_rating',
            field=models.IntegerField(
                default=0,
                verbose_name='Are you satisfied with the number of people that visited your stand?',
                choices=[
                    (0, 'Did not use'), (1, '1: Very bad'), (2, '2: Bad'),
                    (3, '3: Not bad or good'), (4, '4: Good'), (5, '5: Very good')
                ]
            ),
        ),
        migrations.AlterField(
            model_name='issue',
            name='app',
            field=models.CharField(
                max_length=50, verbose_name='app', choices=[
                    (b'all', 'All'), (b'admin', 'Admin'), (b'company', 'BDB'),
                    (b'career', 'Career'), (b'core', 'Core'), (b'events', 'Events'),
                    (b'feedback', 'Feedback'), (b'frontpage', 'Frontpage'),
                    (b'logistics', 'Logistics'), (b'mail', 'Mail'), (b'meetings', 'Meetings'),
                    (b'news', 'News'), (b'notifications', 'Notifications'), (b'pages', 'Pages'),
                    (b'profiles', 'Profiles'), (b'todo', 'Todo'), (b'venue', 'Venue'),
                    (b'workschedule', 'Workschedule')
                ]
            ),
        ),
    ]

from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_user_year'),
        ('meetings', '0002_meeting_agenda'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='preference',
            field=models.ForeignKey(
                verbose_name='Preference', on_delete=models.SET_NULL, blank=True,
                to='core.Preference', null=True
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='replymeeting',
            name='is_attending',
            field=models.NullBooleanField(verbose_name='attending'),
        ),
    ]

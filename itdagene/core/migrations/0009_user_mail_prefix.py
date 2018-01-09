from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_user_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='mail_prefix',
            field=models.CharField(
                default='', help_text=
                'This is a mail prefix for your itdagene mail. The address will be value@itdagene.no.',
                max_length=40, verbose_name='Mail prefix'
            ),
            preserve_default=True,
        ),
    ]

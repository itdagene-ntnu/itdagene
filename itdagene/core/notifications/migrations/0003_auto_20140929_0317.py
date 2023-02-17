from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("notifications", "0002_remove_notification_sent_mail")]

    operations = [
        migrations.AddField(
            model_name="notification",
            name="read",
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="notification",
            name="sent_mail",
            field=models.BooleanField(default=True,
                                      verbose_name="sendt epost"),
            preserve_default=True,
        ),
    ]

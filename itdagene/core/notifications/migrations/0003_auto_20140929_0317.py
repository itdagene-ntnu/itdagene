from django.db import migrations
from django.db.migrations import AddField
from django.db.models import BooleanField


class Migration(migrations.Migration):
    dependencies = [("notifications", "0002_remove_notification_sent_mail")]

    operations = [
        AddField(
            model_name="notification",
            name="read",
            field=BooleanField(default=True),
            preserve_default=True,
        ),
        AddField(
            model_name="notification",
            name="sent_mail",
            field=BooleanField(default=True, verbose_name="sendt epost"),
            preserve_default=True,
        ),
    ]

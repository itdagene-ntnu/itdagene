from django.db import migrations
from django.db.migrations import AddField
from django.db.models import BooleanField


class Migration(migrations.Migration):
    dependencies = [("core", "0011_preference_development_mode")]

    operations = [
        AddField(
            model_name="user",
            name="mail_notification",
            field=BooleanField(default=True, verbose_name="Send mail notifications"),
            preserve_default=True,
        )
    ]

from django.db import migrations
from django.db.migrations import AddField
from django.db.models import PositiveIntegerField


class Migration(migrations.Migration):
    dependencies = [("core", "0012_user_mail_notification")]

    operations = [
        AddField(
            model_name="user",
            name="year",
            field=PositiveIntegerField(
                default=2014,
                help_text="Year the user was active.",
                max_length=3000,
                verbose_name="Active Year",
            ),
            preserve_default=True,
        )
    ]

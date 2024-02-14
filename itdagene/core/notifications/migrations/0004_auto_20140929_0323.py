from django.db import migrations
from django.db.migrations import AlterField
from django.db.models import BooleanField


class Migration(migrations.Migration):
    dependencies = [("notifications", "0003_auto_20140929_0317")]

    operations = [
        AlterField(
            model_name="notification",
            name="sent_mail",
            field=BooleanField(default=False, verbose_name="sendt epost"),
        )
    ]

from django.db import migrations
from django.db.migrations import AlterField
from django.db.models import BooleanField


class Migration(migrations.Migration):
    dependencies = [("notifications", "0004_auto_20140929_0323")]

    operations = [
        AlterField(
            model_name="notification",
            name="read",
            field=BooleanField(default=False),
        )
    ]

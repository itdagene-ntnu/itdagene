from django.conf import settings
from django.db import migrations
from django.db.migrations import AlterField
from django.db.models import ManyToManyField, PositiveIntegerField


class Migration(migrations.Migration):
    dependencies = [("notifications", "0009_auto_20150506_1634")]

    operations = [
        AlterField(
            model_name="notification",
            name="priority",
            field=PositiveIntegerField(
                choices=[(0, "Low"), (1, "Medium"), (2, "High")],
                default=1,
                verbose_name="prioritet",
            ),
        ),
        AlterField(
            model_name="notification",
            name="users",
            field=ManyToManyField(
                related_name="notifications",
                to=settings.AUTH_USER_MODEL,
                verbose_name="users",
            ),
        ),
    ]

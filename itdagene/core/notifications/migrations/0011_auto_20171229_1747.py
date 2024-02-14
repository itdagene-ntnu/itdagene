from django.conf import settings
from django.db import migrations
from django.db.migrations import AlterField
from django.db.models import ManyToManyField


class Migration(migrations.Migration):
    dependencies = [("notifications", "0010_auto_20161004_1437")]

    operations = [
        AlterField(
            model_name="subscription",
            name="subscribers",
            field=ManyToManyField(
                blank=True,
                related_name="subscriptions",
                to=settings.AUTH_USER_MODEL,
            ),
        )
    ]

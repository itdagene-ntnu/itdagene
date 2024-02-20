from __future__ import unicode_literals

from django.db import migrations
from django.db.migrations import AlterField
from django.db.models import PositiveIntegerField


class Migration(migrations.Migration):
    dependencies = [("log", "0002_auto_20140930_1534")]

    operations = [
        AlterField(
            model_name="logitem",
            name="priority",
            field=PositiveIntegerField(
                choices=[
                    (0, "Low"),
                    (1, "Medium"),
                    (2, "High"),
                    (3, "Very High. Will send email to administrators"),
                ],
                default=1,
                verbose_name="priority",
            ),
        )
    ]

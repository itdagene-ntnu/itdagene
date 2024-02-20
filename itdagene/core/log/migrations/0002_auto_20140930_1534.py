from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations
from django.db.migrations import AlterField
from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    PositiveIntegerField,
)


class Migration(migrations.Migration):
    dependencies = [("log", "0001_initial")]

    operations = [
        AlterField(
            model_name="logitem",
            name="action",
            field=CharField(max_length=16, verbose_name="action"),
        ),
        AlterField(
            model_name="logitem",
            name="priority",
            field=PositiveIntegerField(
                default=1,
                verbose_name="priority",
                choices=[
                    (0, "Low"),
                    (1, "Medium"),
                    (2, "High"),
                    (3, "Very High. Will send email to administrators"),
                ],
            ),
        ),
        AlterField(
            model_name="logitem",
            name="timestamp",
            field=DateTimeField(auto_now=True, verbose_name="date"),
        ),
        AlterField(
            model_name="logitem",
            name="user",
            field=ForeignKey(
                verbose_name="user",
                on_delete=CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]

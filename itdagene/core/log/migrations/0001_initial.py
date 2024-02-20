from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations
from django.db.migrations import CreateModel, swappable_dependency
from django.db.models import (
    CASCADE,
    AutoField,
    CharField,
    DateTimeField,
    ForeignKey,
    Model,
    PositiveIntegerField,
)


class Migration(migrations.Migration):
    dependencies = [
        swappable_dependency(settings.AUTH_USER_MODEL),
        ("contenttypes", "0001_initial"),
    ]

    operations = [
        CreateModel(
            name="LogItem",
            fields=[
                (
                    "id",
                    AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "priority",
                    PositiveIntegerField(
                        default=1,
                        verbose_name="prioritet",
                        choices=[
                            (0, "Low"),
                            (1, "Medium"),
                            (2, "High"),
                            (3, "Very High. Will send email to administrators"),
                        ],
                    ),
                ),
                (
                    "timestamp",
                    DateTimeField(auto_now=True, verbose_name="dato"),
                ),
                ("action", CharField(max_length=16, verbose_name="handling")),
                ("object_id", PositiveIntegerField()),
                (
                    "content_type",
                    ForeignKey(to="contenttypes.ContentType", on_delete=CASCADE),
                ),
                (
                    "user",
                    ForeignKey(
                        verbose_name="bruker",
                        on_delete=CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={},
            bases=(Model,),
        )
    ]

from django.conf import settings
from django.db import migrations
from django.db.migrations import CreateModel, swappable_dependency
from django.db.models import (
    CASCADE,
    AutoField,
    BooleanField,
    DateTimeField,
    ForeignKey,
    ManyToManyField,
    Model,
    PositiveIntegerField,
    TextField,
)


class Migration(migrations.Migration):
    dependencies = [
        swappable_dependency(settings.AUTH_USER_MODEL),
        ("contenttypes", "0001_initial"),
    ]

    operations = [
        CreateModel(
            name="Notification",
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
                        choices=[(0, "Low"), (1, "Medium"), (2, "High")],
                    ),
                ),
                ("date", DateTimeField(auto_now=True, verbose_name="dato")),
                ("message", TextField(verbose_name="melding")),
                ("object_id", PositiveIntegerField()),
                (
                    "send_mail",
                    BooleanField(default=True, verbose_name="send epost"),
                ),
                (
                    "sent_mail",
                    BooleanField(default=False, verbose_name="sendt epost"),
                ),
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
        ),
        CreateModel(
            name="Subscription",
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
                ("object_id", PositiveIntegerField()),
                (
                    "content_type",
                    ForeignKey(to="contenttypes.ContentType", on_delete=CASCADE),
                ),
                (
                    "subscribers",
                    ManyToManyField(
                        related_name="subscriptions",
                        null=True,
                        to=settings.AUTH_USER_MODEL,
                        blank=True,
                    ),
                ),
            ],
            options={},
            bases=(Model,),
        ),
    ]

from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("contenttypes", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Notification",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "priority",
                    models.PositiveIntegerField(
                        default=1,
                        verbose_name="prioritet",
                        choices=[(0, b"Low"), (1, b"Medium"), (2, b"High")],
                    ),
                ),
                ("date", models.DateTimeField(auto_now=True, verbose_name="dato")),
                ("message", models.TextField(verbose_name="melding")),
                ("object_id", models.PositiveIntegerField()),
                (
                    "send_mail",
                    models.BooleanField(default=True, verbose_name="send epost"),
                ),
                (
                    "sent_mail",
                    models.BooleanField(default=False, verbose_name="sendt epost"),
                ),
                (
                    "content_type",
                    models.ForeignKey(
                        to="contenttypes.ContentType", on_delete=models.CASCADE
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        verbose_name="bruker",
                        on_delete=models.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Subscription",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("object_id", models.PositiveIntegerField()),
                (
                    "content_type",
                    models.ForeignKey(
                        to="contenttypes.ContentType", on_delete=models.CASCADE
                    ),
                ),
                (
                    "subscribers",
                    models.ManyToManyField(
                        related_name="subscriptions",
                        null=True,
                        to=settings.AUTH_USER_MODEL,
                        blank=True,
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
    ]

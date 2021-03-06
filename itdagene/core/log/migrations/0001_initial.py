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
            name="LogItem",
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
                        choices=[
                            (0, b"Low"),
                            (1, b"Medium"),
                            (2, b"High"),
                            (3, b"Very High. Will send email to administrators"),
                        ],
                    ),
                ),
                ("timestamp", models.DateTimeField(auto_now=True, verbose_name="dato")),
                ("action", models.CharField(max_length=16, verbose_name="handling")),
                ("object_id", models.PositiveIntegerField()),
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
        )
    ]

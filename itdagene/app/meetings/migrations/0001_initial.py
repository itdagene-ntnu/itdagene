from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="Meeting",
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
                ("date_created", models.DateTimeField(editable=False)),
                ("date_saved", models.DateTimeField(editable=False)),
                ("date", models.DateField(verbose_name="date")),
                ("start_time", models.TimeField(verbose_name="from time")),
                (
                    "end_time",
                    models.TimeField(null=True, verbose_name="to time", blank=True),
                ),
                (
                    "type",
                    models.PositiveIntegerField(
                        default=0,
                        verbose_name="type",
                        choices=[
                            (0, "Board meeting"),
                            (1, "Web"),
                            (2, "Banquet"),
                            (3, "Logistics"),
                            (4, "Marketing"),
                            (5, "Other"),
                        ],
                    ),
                ),
                (
                    "location",
                    models.CharField(
                        max_length=40, verbose_name="location", blank=True
                    ),
                ),
                (
                    "abstract",
                    models.TextField(null=True, verbose_name="abstract", blank=True),
                ),
                (
                    "is_board_meeting",
                    models.BooleanField(default=True, verbose_name="is board meeting"),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        related_name="meeting_creator",
                        editable=False,
                        to=settings.AUTH_USER_MODEL,
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "referee",
                    models.ForeignKey(
                        related_name="refereed_meetings",
                        verbose_name="referee",
                        blank=True,
                        on_delete=models.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
                (
                    "saved_by",
                    models.ForeignKey(
                        related_name="meeting_saved_by",
                        editable=False,
                        on_delete=models.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"verbose_name": "meeting", "verbose_name_plural": "meetings"},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Penalty",
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
                ("date_created", models.DateTimeField(editable=False)),
                ("date_saved", models.DateTimeField(editable=False)),
                (
                    "type",
                    models.CharField(
                        default="beer",
                        max_length=10,
                        verbose_name="type",
                        choices=[(b"beer", "Beer"), (b"wine", "Wine")],
                    ),
                ),
                (
                    "bottles",
                    models.PositiveIntegerField(
                        default=2, verbose_name="number of bottles"
                    ),
                ),
                ("reason", models.TextField(verbose_name="reason")),
                (
                    "creator",
                    models.ForeignKey(
                        related_name="penalty_creator",
                        editable=False,
                        to=settings.AUTH_USER_MODEL,
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "meeting",
                    models.ForeignKey(
                        verbose_name="meeting",
                        blank=True,
                        to="meetings.Meeting",
                        null=True,
                        on_delete=models.SET_NULL,
                    ),
                ),
                (
                    "saved_by",
                    models.ForeignKey(
                        related_name="penalty_saved_by",
                        editable=False,
                        to=settings.AUTH_USER_MODEL,
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        related_name="penalties",
                        verbose_name="person",
                        to=settings.AUTH_USER_MODEL,
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={"abstract": False},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="ReplyMeeting",
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
                ("date_created", models.DateTimeField(editable=False)),
                ("date_saved", models.DateTimeField(editable=False)),
                (
                    "is_attending",
                    models.NullBooleanField(default=False, verbose_name="attending"),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        related_name="replymeeting_creator",
                        editable=False,
                        to=settings.AUTH_USER_MODEL,
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "meeting",
                    models.ForeignKey(
                        related_name="replies",
                        verbose_name="meeting",
                        to="meetings.Meeting",
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "saved_by",
                    models.ForeignKey(
                        related_name="replymeeting_saved_by",
                        editable=False,
                        to=settings.AUTH_USER_MODEL,
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        verbose_name="user",
                        to=settings.AUTH_USER_MODEL,
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={"abstract": False},
            bases=(models.Model,),
        ),
    ]

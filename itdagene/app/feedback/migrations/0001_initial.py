from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("company", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Evaluation",
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
                    "internship_marathon_rating",
                    models.IntegerField(
                        default=0,
                        verbose_name="How did the kickstart go?",
                        choices=[
                            (0, "Did not use"),
                            (1, "1: Very bad"),
                            (2, "2: Bad"),
                            (3, "3: Not bad or good"),
                            (4, "4: Good"),
                            (5, "5: Very good"),
                        ],
                    ),
                ),
                (
                    "internship_marathon_improvement",
                    models.TextField(
                        verbose_name="What could have been done better at the kickstart?"
                    ),
                ),
                (
                    "course_rating",
                    models.IntegerField(
                        default=0,
                        verbose_name="How did the course go?",
                        choices=[
                            (0, "Did not use"),
                            (1, "1: Very bad"),
                            (2, "2: Bad"),
                            (3, "3: Not bad or good"),
                            (4, "4: Good"),
                            (5, "5: Very good"),
                        ],
                    ),
                ),
                (
                    "course_improvement",
                    models.TextField(
                        verbose_name="Could the course be handled better?"
                    ),
                ),
                (
                    "visitors_rating",
                    models.IntegerField(
                        verbose_name="Are you satisfied with the number of people that visited your stand?",
                        choices=[
                            (0, "Did not use"),
                            (1, "1: Very bad"),
                            (2, "2: Bad"),
                            (3, "3: Not bad or good"),
                            (4, "4: Good"),
                            (5, "5: Very good"),
                        ],
                    ),
                ),
                (
                    "has_interview_location",
                    models.BooleanField(
                        default=False, verbose_name="Did you use interview rooms?"
                    ),
                ),
                (
                    "interview_location_rating",
                    models.IntegerField(
                        default=0,
                        verbose_name="How was the interview room?",
                        choices=[
                            (0, "Did not use"),
                            (1, "1: Very bad"),
                            (2, "2: Bad"),
                            (3, "3: Not bad or good"),
                            (4, "4: Good"),
                            (5, "5: Very good"),
                        ],
                    ),
                ),
                (
                    "interview_location_improvement",
                    models.TextField(
                        verbose_name="What could have been done better?", blank=True
                    ),
                ),
                (
                    "has_banquet",
                    models.BooleanField(
                        default=False, verbose_name="Where you at the banquet?"
                    ),
                ),
                (
                    "banquet_rating",
                    models.IntegerField(
                        default=0,
                        verbose_name="How did the banquet go?",
                        choices=[
                            (0, "Did not use"),
                            (1, "1: Very bad"),
                            (2, "2: Bad"),
                            (3, "3: Not bad or good"),
                            (4, "4: Good"),
                            (5, "5: Very good"),
                        ],
                    ),
                ),
                (
                    "banquet_improvement",
                    models.TextField(
                        verbose_name="What could have been done better at the banquet?",
                        blank=True,
                    ),
                ),
                (
                    "opening_hours",
                    models.TextField(
                        verbose_name="Was the opening hours(10-16) ok? If not what would be your choice?"
                    ),
                ),
                (
                    "improvement",
                    models.TextField(verbose_name="What could have been done better?"),
                ),
                (
                    "other",
                    models.TextField(
                        help_text="Do you have any tips?",
                        verbose_name="Something else you want to comment?",
                        blank=True,
                    ),
                ),
                (
                    "want_to_come_back",
                    models.BooleanField(
                        default=False,
                        verbose_name="Interested in being contacted next year?",
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="EvaluationHash",
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
                ("hash", models.CharField(unique=True, max_length=250)),
                (
                    "company",
                    models.ForeignKey(to="company.Company", on_delete=models.CASCADE),
                ),
                (
                    "preference",
                    models.ForeignKey(to="core.Preference", on_delete=models.CASCADE),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Issue",
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
                ("title", models.CharField(max_length=100, verbose_name="title")),
                (
                    "app",
                    models.CharField(
                        max_length=50,
                        verbose_name="app",
                        choices=[
                            (b"all", "All"),
                            (b"admin", "Admin"),
                            (b"company", "BDB"),
                            (b"career", "Career"),
                            (b"core", "Core"),
                            (b"documents", "Documents"),
                            (b"events", "Events"),
                            (b"feedback", "Feedback"),
                            (b"frontpage", "Frontpage"),
                            (b"logistics", "Logistics"),
                            (b"meetings", "Meetings"),
                            (b"news", "News"),
                            (b"notifications", "Notifications"),
                            (b"pages", "Pages"),
                            (b"profiles", "Profiles"),
                            (b"todo", "Todo"),
                            (b"venue", "Venue"),
                            (b"workschedule", "Workschedule"),
                        ],
                    ),
                ),
                (
                    "type",
                    models.PositiveIntegerField(
                        default=1,
                        verbose_name="type",
                        choices=[(0, "Bug"), (1, "Feature"), (2, "Cache problem")],
                    ),
                ),
                (
                    "status",
                    models.PositiveIntegerField(
                        default=0,
                        verbose_name="status",
                        choices=[
                            (0, "New"),
                            (1, "In progress"),
                            (2, "Needs feedback"),
                            (3, "Finished"),
                        ],
                    ),
                ),
                ("description", models.TextField(verbose_name="description")),
                (
                    "is_solved",
                    models.BooleanField(default=False, verbose_name="is solved"),
                ),
                (
                    "deadline",
                    models.DateTimeField(
                        null=True, verbose_name="deadline", blank=True
                    ),
                ),
                (
                    "solved_date",
                    models.DateTimeField(
                        null=True, verbose_name="solved date", blank=True
                    ),
                ),
                (
                    "assigned_user",
                    models.ForeignKey(
                        related_name="assigned_issues",
                        verbose_name="assigned user",
                        blank=True,
                        on_delete=models.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        related_name="issue_creator",
                        editable=False,
                        to=settings.AUTH_USER_MODEL,
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "saved_by",
                    models.ForeignKey(
                        related_name="issue_saved_by",
                        editable=False,
                        to=settings.AUTH_USER_MODEL,
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
            options={"verbose_name": "issue", "verbose_name_plural": "issues"},
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name="evaluationhash", unique_together=set([("preference", "company")])
        ),
        migrations.AddField(
            model_name="evaluation",
            name="hash",
            field=models.ForeignKey(
                to="feedback.EvaluationHash", on_delete=models.CASCADE
            ),
            preserve_default=True,
        ),
    ]

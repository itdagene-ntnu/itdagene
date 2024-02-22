from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("company", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Milestone",
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
                ("title", models.CharField(max_length=80, verbose_name="title")),
                ("description", models.TextField(verbose_name="description")),
                ("deadline", models.DateTimeField(verbose_name="deadline")),
                (
                    "todo_per_company",
                    models.BooleanField(
                        default=False,
                        help_text="If unchecked there will only be created a todo for each board-user",
                        verbose_name="todo for each company",
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        related_name="milestone_creator",
                        editable=False,
                        on_delete=models.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "saved_by",
                    models.ForeignKey(
                        related_name="milestone_saved_by",
                        editable=False,
                        on_delete=models.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"abstract": False},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Todo",
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
                ("title", models.CharField(max_length=80, verbose_name="title")),
                (
                    "description",
                    models.TextField(verbose_name="description", blank=True),
                ),
                (
                    "deadline",
                    models.DateTimeField(
                        null=True, verbose_name="deadline", blank=True
                    ),
                ),
                (
                    "finished",
                    models.BooleanField(default=False, verbose_name="finished"),
                ),
                (
                    "company",
                    models.ForeignKey(
                        related_name="todos",
                        verbose_name="company",
                        blank=True,
                        on_delete=models.SET_NULL,
                        to="company.Company",
                        null=True,
                    ),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        related_name="todo_creator",
                        editable=False,
                        to=settings.AUTH_USER_MODEL,
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "milestone",
                    models.ForeignKey(
                        related_name="todos",
                        verbose_name="milestone",
                        blank=True,
                        on_delete=models.SET_NULL,
                        to="todo.Milestone",
                        null=True,
                    ),
                ),
                (
                    "saved_by",
                    models.ForeignKey(
                        related_name="todo_saved_by",
                        editable=False,
                        to=settings.AUTH_USER_MODEL,
                        on_delete=models.CASCADE,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        related_name="todos",
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

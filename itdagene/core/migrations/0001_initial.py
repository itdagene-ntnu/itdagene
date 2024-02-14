from django.conf import settings
from django.core.validators import RegexValidator
from django.db import migrations
from django.db.migrations import CreateModel
from django.db.models import (
    CASCADE,
    AutoField,
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    EmailField,
    ForeignKey,
    IntegerField,
    ManyToManyField,
    Model,
    PositiveIntegerField,
)
from django.utils.timezone import now


class Migration(migrations.Migration):
    dependencies = [("auth", "0001_initial")]

    operations = [
        CreateModel(
            name="User",
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
                    "password",
                    CharField(max_length=128, verbose_name="password"),
                ),
                (
                    "last_login",
                    DateTimeField(default=now, verbose_name="last login"),
                ),
                (
                    "is_superuser",
                    BooleanField(
                        default=False,
                        help_text=(
                            "Designates that this user has all permissions "
                            "without explicitly assigning them."
                        ),
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    CharField(
                        help_text=(
                            "Required. 30 characters or fewer. Letters, "
                            "digits and @/./+/-/_ only."
                        ),
                        unique=True,
                        max_length=30,
                        verbose_name="username",
                        validators=[
                            RegexValidator(
                                "^[\\w.@+-]+$",
                                "Enter a valid username.",
                                "invalid",
                            )
                        ],
                    ),
                ),
                (
                    "first_name",
                    CharField(max_length=30, verbose_name="first name", blank=True),
                ),
                (
                    "last_name",
                    CharField(max_length=30, verbose_name="last name", blank=True),
                ),
                (
                    "email",
                    EmailField(max_length=75, verbose_name="email address", blank=True),
                ),
                (
                    "is_staff",
                    BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    BooleanField(
                        default=True,
                        help_text=(
                            "Designates whether this user should be treated "
                            "as active. Unselect this instead of deleting "
                            "accounts."
                        ),
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    DateTimeField(default=now, verbose_name="date joined"),
                ),
                (
                    "groups",
                    ManyToManyField(
                        related_query_name="user",
                        related_name="user_set",
                        to="auth.Group",
                        blank=True,
                        help_text=(
                            "The groups this user belongs to. A user will get "
                            "all permissions granted to each of his/her group."
                        ),
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    ManyToManyField(
                        related_query_name="user",
                        related_name="user_set",
                        to="auth.Permission",
                        blank=True,
                        help_text="Specific permissions for this user.",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "abstract": False,
                "verbose_name": "user",
                "verbose_name_plural": "users",
            },
            bases=(Model,),
        ),
        CreateModel(
            name="Preference",
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
                ("date_created", DateTimeField(editable=False)),
                ("date_saved", DateTimeField(editable=False)),
                ("active", BooleanField(default=False, verbose_name="active")),
                (
                    "year",
                    IntegerField(null=True, verbose_name="year", blank=True),
                ),
                ("start_date", DateField(verbose_name="start date")),
                ("end_date", DateField(verbose_name="end date")),
                (
                    "nr_of_stands",
                    PositiveIntegerField(
                        default=30,
                        help_text="This is for each day, not the sum of each day",
                        verbose_name="number of stands",
                    ),
                ),
                (
                    "view_sp",
                    BooleanField(default=False, verbose_name="view partners"),
                ),
                (
                    "creator",
                    ForeignKey(
                        related_name="preference_creator",
                        on_delete=CASCADE,
                        editable=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "saved_by",
                    ForeignKey(
                        related_name="preference_saved_by",
                        on_delete=CASCADE,
                        editable=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Preference",
                "verbose_name_plural": "Preferences",
            },
            bases=(Model,),
        ),
        CreateModel(
            name="UserProxy",
            fields=[],
            options={"proxy": True},
            bases=("core.user",),
        ),
    ]

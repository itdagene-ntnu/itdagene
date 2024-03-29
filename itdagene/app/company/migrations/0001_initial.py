from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CallTeam",
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
            ],
            options={"abstract": False},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Comment",
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
                ("timestamp", models.DateTimeField(verbose_name="timestamp")),
                ("content", models.TextField(verbose_name="content")),
            ],
            options={"verbose_name": "comment", "verbose_name_plural": "comments"},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Company",
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
                ("name", models.CharField(max_length=140, verbose_name="name")),
                ("url", models.URLField(null=True, verbose_name="url", blank=True)),
                ("phone", models.CharField(max_length=20, null=True, blank=True)),
                (
                    "logo",
                    models.ImageField(
                        upload_to="company_logos/",
                        null=True,
                        verbose_name="logo",
                        blank=True,
                    ),
                ),
                (
                    "status",
                    models.PositiveIntegerField(
                        default=0,
                        verbose_name="status",
                        choices=[
                            (0, "Not contacted"),
                            (4, "Contacted"),
                            (1, "Not interested"),
                            (2, "Interested"),
                            (3, "Signed"),
                        ],
                    ),
                ),
                (
                    "description",
                    models.TextField(verbose_name="description", blank=True),
                ),
                ("address", models.TextField(verbose_name="address", blank=True)),
                (
                    "payment_address",
                    models.TextField(verbose_name="payment address", blank=True),
                ),
                ("fax", models.CharField(max_length=20, null=True, blank=True)),
                ("active", models.BooleanField(default=True, verbose_name="active")),
                (
                    "has_public_profile",
                    models.BooleanField(default=False, verbose_name="profile"),
                ),
                ("mp", models.BooleanField(default=False, verbose_name="Main partner")),
                ("partner", models.BooleanField(default=False, verbose_name="Partner")),
            ],
            options={"ordering": ("name",)},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="CompanyContact",
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
                    "first_name",
                    models.CharField(
                        max_length=30, verbose_name="first name", blank=True
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        max_length=30, verbose_name="last name", blank=True
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=75, verbose_name="e-mail address", blank=True
                    ),
                ),
                (
                    "phone",
                    models.CharField(
                        max_length=20,
                        null=True,
                        verbose_name="phone number",
                        blank=True,
                    ),
                ),
                (
                    "mobile_phone",
                    models.CharField(
                        max_length=20,
                        null=True,
                        verbose_name="phone number",
                        blank=True,
                    ),
                ),
                (
                    "position",
                    models.CharField(
                        max_length=60, verbose_name="position", blank=True
                    ),
                ),
            ],
            options={
                "verbose_name": "company contact",
                "verbose_name_plural": "company contacts",
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Contract",
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
                    "timestamp",
                    models.DateTimeField(
                        help_text="Signing date, not uploaded date", verbose_name="date"
                    ),
                ),
                (
                    "file",
                    models.FileField(
                        upload_to="contracts/",
                        null=True,
                        verbose_name="file",
                        blank=True,
                    ),
                ),
                (
                    "banquet_tickets",
                    models.PositiveIntegerField(
                        default=1, verbose_name="banquet tickets"
                    ),
                ),
                (
                    "joblistings",
                    models.PositiveIntegerField(default=2, verbose_name="joblistings"),
                ),
                (
                    "interview_room",
                    models.PositiveIntegerField(
                        default=0, verbose_name="interview room"
                    ),
                ),
                (
                    "is_billed",
                    models.BooleanField(default=False, verbose_name="is billed"),
                ),
                (
                    "has_paid",
                    models.BooleanField(default=False, verbose_name="has paid"),
                ),
            ],
            options={"verbose_name": "contract", "verbose_name_plural": "contracts"},
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name="Package",
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
                ("name", models.CharField(max_length=40, verbose_name="name")),
                (
                    "description",
                    models.TextField(
                        help_text="This field supports markdown",
                        verbose_name="description",
                    ),
                ),
                ("price", models.PositiveIntegerField(verbose_name="price")),
                (
                    "max",
                    models.PositiveIntegerField(
                        null=True, verbose_name="number of packages to sell", blank=True
                    ),
                ),
                ("has_stand_first_day", models.BooleanField(default=False)),
                ("has_stand_last_day", models.BooleanField(default=False)),
                (
                    "has_waiting_list",
                    models.BooleanField(default=True, verbose_name="has waiting list"),
                ),
                (
                    "includes_course",
                    models.BooleanField(default=False, verbose_name="includes course"),
                ),
                ("is_full", models.BooleanField(default=False, verbose_name="is full")),
            ],
            options={
                "ordering": ("name",),
                "verbose_name": "package",
                "verbose_name_plural": "packages",
            },
            bases=(models.Model,),
        ),
    ]

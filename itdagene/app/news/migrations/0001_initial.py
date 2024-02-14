from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="Announcement",
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
                ("content", models.TextField(verbose_name="content")),
                (
                    "image",
                    models.ImageField(upload_to="announcements/", verbose_name="image"),
                ),
                (
                    "creator",
                    models.ForeignKey(
                        related_name="announcement_creator",
                        on_delete=models.CASCADE,
                        editable=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "saved_by",
                    models.ForeignKey(
                        related_name="announcement_saved_by",
                        on_delete=models.CASCADE,
                        editable=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "announcement",
                "verbose_name_plural": "announcements",
            },
            bases=(models.Model,),
        )
    ]

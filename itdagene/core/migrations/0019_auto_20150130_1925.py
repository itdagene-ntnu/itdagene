from django.db import migrations
from django.db.migrations import AlterField
from django.db.models import CharField, ImageField, PositiveIntegerField


class Migration(migrations.Migration):
    dependencies = [("core", "0018_delete_userproxy")]

    operations = [
        AlterField(
            model_name="user",
            name="language",
            field=CharField(
                default="nb",
                max_length=3,
                verbose_name="Language",
                choices=[("nb", "Norsk"), ("en", "English")],
            ),
        ),
        AlterField(
            model_name="user",
            name="photo",
            field=ImageField(
                upload_to="photos/users/", null=True, verbose_name="Photo", blank=True
            ),
        ),
        AlterField(
            model_name="user",
            name="year",
            field=PositiveIntegerField(
                default=2015,
                max_length=3000,
                blank=True,
                help_text="Year the user was active.",
                null=True,
                verbose_name="Active Year",
            ),
        ),
    ]

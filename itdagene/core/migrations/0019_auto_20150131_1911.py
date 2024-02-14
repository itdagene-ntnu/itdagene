from django.db import migrations
from django.db.migrations import AlterField
from django.db.models import PositiveIntegerField


class Migration(migrations.Migration):
    dependencies = [("core", "0018_delete_userproxy")]

    operations = [
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
        )
    ]

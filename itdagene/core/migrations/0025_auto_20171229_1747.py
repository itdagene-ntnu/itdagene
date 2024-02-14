from django.db import migrations
from django.db.migrations import AlterField
from django.db.models import PositiveIntegerField


class Migration(migrations.Migration):
    dependencies = [("core", "0024_merge_20171229_1651")]

    operations = [
        AlterField(
            model_name="user",
            name="year",
            field=PositiveIntegerField(
                blank=True,
                default=2017,
                help_text="Year the user was active.",
                null=True,
                verbose_name="Active Year",
            ),
        )
    ]

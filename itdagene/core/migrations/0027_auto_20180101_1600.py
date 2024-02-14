from django.db import migrations
from django.db.migrations import AlterField
from django.db.models import PositiveIntegerField

from itdagene.core.models import user_default_year


class Migration(migrations.Migration):
    dependencies = [("core", "0026_auto_20171231_1831")]

    operations = [
        AlterField(
            model_name="user",
            name="year",
            field=PositiveIntegerField(
                blank=True,
                default=user_default_year,
                help_text="Year the user was active.",
                null=True,
                verbose_name="Active Year",
            ),
        )
    ]

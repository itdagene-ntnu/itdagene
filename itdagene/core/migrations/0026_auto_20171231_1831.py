from django.db import migrations
from django.db.migrations import AlterField
from django.db.models import CharField


class Migration(migrations.Migration):
    dependencies = [("core", "0025_auto_20171229_1747")]

    operations = [
        AlterField(
            model_name="user",
            name="last_name",
            field=CharField(blank=True, max_length=150, verbose_name="last name"),
        )
    ]

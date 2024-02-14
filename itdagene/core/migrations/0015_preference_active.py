from django.db import migrations
from django.db.migrations import AddField
from django.db.models import BooleanField


class Migration(migrations.Migration):
    dependencies = [("core", "0014_remove_preference_active")]

    operations = [
        AddField(
            model_name="preference",
            name="active",
            field=BooleanField(default=False, verbose_name="active"),
            preserve_default=True,
        )
    ]

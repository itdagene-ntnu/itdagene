from django.db import migrations
from django.db.migrations import AddField
from django.db.models import IntegerField


class Migration(migrations.Migration):
    dependencies = [("core", "0001_initial")]

    operations = [
        AddField(
            model_name="user",
            name="phone",
            field=IntegerField(null=True, verbose_name="phone number", blank=True),
            preserve_default=True,
        )
    ]

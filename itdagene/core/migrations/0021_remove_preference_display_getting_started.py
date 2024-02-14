from django.db import migrations
from django.db.migrations import RemoveField


class Migration(migrations.Migration):
    dependencies = [("core", "0020_merge")]

    operations = [RemoveField(model_name="preference", name="display_getting_started")]

from django.db import migrations
from django.db.migrations import RemoveField


class Migration(migrations.Migration):
    dependencies = [("core", "0013_user_year")]

    operations = [RemoveField(model_name="preference", name="active")]

from django.db import migrations
from django.db.migrations import RemoveField


class Migration(migrations.Migration):
    dependencies = [("core", "0016_auto_20141007_2055")]

    operations = [RemoveField(model_name="user", name="mail_prefix")]

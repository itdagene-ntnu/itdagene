from django.db import migrations
from django.db.migrations import RemoveField


class Migration(migrations.Migration):
    dependencies = [("notifications", "0001_initial")]

    operations = [RemoveField(model_name="notification", name="sent_mail")]

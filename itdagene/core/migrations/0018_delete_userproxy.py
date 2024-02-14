from django.db import migrations
from django.db.migrations import DeleteModel


class Migration(migrations.Migration):
    dependencies = [("core", "0017_remove_user_mail_prefix")]

    operations = [DeleteModel(name="UserProxy")]

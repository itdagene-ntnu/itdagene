from django.db import migrations
from django.db.migrations import AlterModelOptions


class Migration(migrations.Migration):
    dependencies = [("core", "0004_preference_display_getting_started")]

    operations = [
        AlterModelOptions(name="user", options={"permissions": ("send_welcome_mail",)})
    ]

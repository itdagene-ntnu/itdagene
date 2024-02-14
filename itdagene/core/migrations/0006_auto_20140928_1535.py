from django.db import migrations
from django.db.migrations import AlterModelOptions


class Migration(migrations.Migration):
    dependencies = [("core", "0005_auto_20140928_1531")]

    operations = [
        AlterModelOptions(
            name="user",
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "permissions": ("send_welcome_mail",),
            },
        )
    ]

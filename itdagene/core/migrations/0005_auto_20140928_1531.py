from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("core", "0004_preference_display_getting_started")]

    operations = [
        migrations.AlterModelOptions(
            name="user", options={"permissions": ("send_welcome_mail",)}
        )
    ]

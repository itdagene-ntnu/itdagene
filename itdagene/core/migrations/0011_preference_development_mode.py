from django.db import migrations
from django.db.migrations import AddField
from django.db.models import BooleanField


class Migration(migrations.Migration):
    dependencies = [("core", "0010_auto_20140928_1748")]

    operations = [
        AddField(
            model_name="preference",
            name="development_mode",
            field=BooleanField(
                default=False,
                help_text=(
                    "This option puts the site in development mode. The "
                    "public page will be disabled."
                ),
                verbose_name="Development Mode",
            ),
            preserve_default=True,
        )
    ]

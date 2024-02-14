from django.db import migrations
from django.db.migrations import AlterField
from django.db.models import CharField


class Migration(migrations.Migration):
    dependencies = [("core", "0009_user_mail_prefix")]

    operations = [
        AlterField(
            model_name="user",
            name="mail_prefix",
            field=CharField(
                default="",
                help_text=(
                    "This is a mail prefix for your itdagene mail. The "
                    "address will be value@itdagene.no. This is typicaly you "
                    "name or username. Don't use a group name."
                ),
                unique=True,
                max_length=40,
                verbose_name="Mail prefix",
            ),
        )
    ]

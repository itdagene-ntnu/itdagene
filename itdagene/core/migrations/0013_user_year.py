from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("core", "0012_user_mail_notification")]

    operations = [
        migrations.AddField(
            model_name="user",
            name="year",
            field=models.PositiveIntegerField(
                default=2014,
                help_text="Year the user was active.",
                max_length=3000,
                verbose_name="Active Year",
            ),
            preserve_default=True,
        )
    ]

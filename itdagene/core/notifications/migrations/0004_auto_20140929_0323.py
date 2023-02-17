from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("notifications", "0003_auto_20140929_0317")]

    operations = [
        migrations.AlterField(
            model_name="notification",
            name="sent_mail",
            field=models.BooleanField(default=False,
                                      verbose_name="sendt epost"),
        )
    ]

from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("notifications", "0008_auto_20150423_0137")]

    operations = [
        migrations.AlterField(
            model_name="notification",
            name="users",
            field=models.ManyToManyField(
                related_name="notifications",
                verbose_name="users",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=True,
        )
    ]

from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("log", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="logitem",
            name="action",
            field=models.CharField(max_length=16, verbose_name="action"),
        ),
        migrations.AlterField(
            model_name="logitem",
            name="priority",
            field=models.PositiveIntegerField(
                default=1,
                verbose_name="priority",
                choices=[
                    (0, b"Low"),
                    (1, b"Medium"),
                    (2, b"High"),
                    (3, b"Very High. Will send email to administrators"),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="logitem",
            name="timestamp",
            field=models.DateTimeField(auto_now=True, verbose_name="date"),
        ),
        migrations.AlterField(
            model_name="logitem",
            name="user",
            field=models.ForeignKey(
                verbose_name="user",
                on_delete=models.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]

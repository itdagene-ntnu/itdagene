from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("notifications", "0006_auto_20141123_2025")]

    operations = [
        migrations.AlterField(
            model_name="notification",
            name="date",
            field=models.DateTimeField(auto_now=True, verbose_name="dato"),
        ),
        migrations.AlterField(
            model_name="notification",
            name="message",
            field=models.TextField(verbose_name="melding"),
        ),
        migrations.AlterField(
            model_name="notification",
            name="priority",
            field=models.PositiveIntegerField(
                default=1,
                verbose_name="prioritet",
                choices=[(0, b"Low"), (1, b"Medium"), (2, b"High")],
            ),
        ),
        migrations.AlterField(
            model_name="notification",
            name="sent_mail",
            field=models.BooleanField(default=False, verbose_name="sendt mail"),
        ),
    ]

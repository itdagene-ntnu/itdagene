from django.db import migrations
from django.db.migrations import AlterField
from django.db.models import (
    BooleanField,
    DateTimeField,
    PositiveIntegerField,
    TextField,
)


class Migration(migrations.Migration):
    dependencies = [("notifications", "0006_auto_20141123_2025")]

    operations = [
        AlterField(
            model_name="notification",
            name="date",
            field=DateTimeField(auto_now=True, verbose_name="dato"),
        ),
        AlterField(
            model_name="notification",
            name="message",
            field=TextField(verbose_name="melding"),
        ),
        AlterField(
            model_name="notification",
            name="priority",
            field=PositiveIntegerField(
                default=1,
                verbose_name="prioritet",
                choices=[(0, "Low"), (1, "Medium"), (2, "High")],
            ),
        ),
        AlterField(
            model_name="notification",
            name="sent_mail",
            field=BooleanField(default=False, verbose_name="sendt mail"),
        ),
    ]

from django.db import migrations
from django.db.migrations import AlterField
from django.db.models import (
    BooleanField,
    DateTimeField,
    PositiveIntegerField,
    TextField,
)


class Migration(migrations.Migration):
    dependencies = [("notifications", "0005_auto_20140929_0353")]

    operations = [
        AlterField(
            model_name="notification",
            name="date",
            field=DateTimeField(auto_now=True, verbose_name="date"),
        ),
        AlterField(
            model_name="notification",
            name="message",
            field=TextField(verbose_name="message"),
        ),
        AlterField(
            model_name="notification",
            name="priority",
            field=PositiveIntegerField(
                default=1,
                verbose_name="priority",
                choices=[(0, "Low"), (1, "Medium"), (2, "High")],
            ),
        ),
        AlterField(
            model_name="notification",
            name="send_mail",
            field=BooleanField(default=True, verbose_name="send mail"),
        ),
        AlterField(
            model_name="notification",
            name="sent_mail",
            field=BooleanField(default=False, verbose_name="sent mail"),
        ),
    ]

from django.db import migrations
from django.db.migrations import AlterField
from django.db.models import BooleanField, DateTimeField, PositiveIntegerField


class Migration(migrations.Migration):
    dependencies = [("notifications", "0011_auto_20171229_1747")]

    operations = [
        AlterField(
            model_name="notification",
            name="date",
            field=DateTimeField(auto_now=True, verbose_name="Dato"),
        ),
        AlterField(
            model_name="notification",
            name="priority",
            field=PositiveIntegerField(
                choices=[(0, "Low"), (1, "Medium"), (2, "High")],
                default=1,
                verbose_name="priority",
            ),
        ),
        AlterField(
            model_name="notification",
            name="sent_mail",
            field=BooleanField(default=False, verbose_name="sent mail"),
        ),
    ]

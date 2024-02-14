from django.db import migrations
from django.db.migrations import AddField
from django.db.models import BooleanField


class Migration(migrations.Migration):
    dependencies = [("core", "0029_auto_20180206_1156")]

    operations = [
        AddField(
            model_name="preference",
            name="view_companies",
            field=BooleanField(default=False, verbose_name="view all comapnies"),
        ),
        AddField(
            model_name="preference",
            name="view_hsp",
            field=BooleanField(default=False, verbose_name="view main collaborator"),
        ),
    ]

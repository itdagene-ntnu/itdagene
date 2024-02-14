from django.db import migrations
from django.db.migrations import AlterField
from django.db.models import BooleanField


class Migration(migrations.Migration):
    dependencies = [("core", "0030_auto_20180729_0107")]

    operations = [
        AlterField(
            model_name="preference",
            name="view_companies",
            field=BooleanField(
                default=False,
                help_text="Should all companies be displayed on the front page?",
                verbose_name="view all comapnies",
            ),
        ),
        AlterField(
            model_name="preference",
            name="view_hsp",
            field=BooleanField(
                default=False,
                help_text="Should the main collaborator be displayed on the front page?",
                verbose_name="view main collaborator",
            ),
        ),
        AlterField(
            model_name="preference",
            name="view_sp",
            field=BooleanField(
                default=False,
                help_text="Should all collaborators be displayed on the front page?",
                verbose_name="view partners",
            ),
        ),
    ]

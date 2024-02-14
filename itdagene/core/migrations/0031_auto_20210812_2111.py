from django.db import migrations
from django.db.migrations import AddField
from django.db.models import BooleanField, URLField


class Migration(migrations.Migration):
    dependencies = [("core", "0030_auto_20180729_0107")]

    operations = [
        AddField(
            model_name="preference",
            name="interest_form_url",
            field=URLField(
                default="https://interesse.itdagene.no",
                help_text="What is the URL to the company participation interest form?",
                verbose_name="Interest form URL",
            ),
        ),
        AddField(
            model_name="preference",
            name="show_interest_form",
            field=BooleanField(
                default=True,
                help_text=(
                    "Should the company participation interest form be "
                    "visible on the front page?"
                ),
                verbose_name="Show interest form",
            ),
        ),
    ]

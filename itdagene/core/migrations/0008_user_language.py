from django.db import migrations
from django.db.migrations import AddField
from django.db.models import CharField


class Migration(migrations.Migration):
    dependencies = [("core", "0007_auto_20140928_1537")]

    operations = [
        AddField(
            model_name="user",
            name="language",
            field=CharField(
                default="nb", max_length=3, choices=[("nb", "Norsk"), ("en", "English")]
            ),
            preserve_default=True,
        )
    ]

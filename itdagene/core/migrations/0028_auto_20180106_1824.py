from django.db import migrations
from django.db.migrations import AlterField
from django.db.models import CharField


class Migration(migrations.Migration):
    dependencies = [("core", "0027_auto_20180101_1600")]

    operations = [
        AlterField(
            model_name="user",
            name="language",
            field=CharField(
                choices=[("nb", "Norsk")],
                default="nb",
                max_length=3,
                verbose_name="Language",
            ),
        )
    ]

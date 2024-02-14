from django.db import migrations
from django.db.migrations import AddField
from django.db.models import ImageField


class Migration(migrations.Migration):
    dependencies = [("core", "0002_user_phone")]

    operations = [
        AddField(
            model_name="user",
            name="photo",
            field=ImageField(null=True, upload_to="photos/users/", blank=True),
            preserve_default=True,
        )
    ]

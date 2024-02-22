from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("core", "0013_user_year")]

    operations = [migrations.RemoveField(model_name="preference", name="active")]

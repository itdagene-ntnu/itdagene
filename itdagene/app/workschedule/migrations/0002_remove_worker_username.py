from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("workschedule", "0001_initial")]

    operations = [migrations.RemoveField(model_name="worker", name="username")]

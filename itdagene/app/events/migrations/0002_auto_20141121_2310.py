from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("events", "0001_initial")]

    operations = [
        migrations.AlterModelOptions(name="ticket",
                                     options={"ordering": ("last_name", )}),
        migrations.RemoveField(model_name="ticket", name="user"),
    ]

from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("todo", "0001_initial")]

    operations = [
        migrations.RemoveField(model_name="milestone", name="creator"),
        migrations.RemoveField(model_name="milestone", name="saved_by"),
        migrations.RemoveField(model_name="todo", name="company"),
        migrations.RemoveField(model_name="todo", name="milestone"),
        migrations.DeleteModel(name="Milestone"),
    ]

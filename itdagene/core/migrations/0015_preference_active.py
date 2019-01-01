from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("core", "0014_remove_preference_active")]

    operations = [
        migrations.AddField(
            model_name="preference",
            name="active",
            field=models.BooleanField(default=False, verbose_name="active"),
            preserve_default=True,
        )
    ]

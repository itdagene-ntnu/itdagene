from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("meetings", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="meeting",
            name="agenda",
            field=models.TextField(
                null=True, verbose_name="Meeting Agenda", blank=True
            ),
            preserve_default=True,
        )
    ]

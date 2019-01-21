from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("career", "0006_auto_20141121_2054")]

    operations = [
        migrations.AddField(
            model_name="joblisting",
            name="frontpage",
            field=models.BooleanField(default=False, verbose_name="Frontpage"),
            preserve_default=True,
        )
    ]

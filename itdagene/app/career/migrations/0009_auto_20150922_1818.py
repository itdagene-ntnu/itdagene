from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("career", "0008_merge")]

    operations = [
        migrations.AlterModelOptions(
            name="joblisting", options={"ordering": ("deadline",)}
        )
    ]

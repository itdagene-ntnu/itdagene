from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("company", "0009_auto_20150506_1634")]

    operations = [
        migrations.AddField(
            model_name="company",
            name="is_collaborator",
            field=models.BooleanField(default=False, verbose_name="collaborator"),
            preserve_default=True,
        )
    ]

from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("career", "0003_auto_20141121_2006")]

    operations = [
        migrations.RenameField(model_name="joblisting",
                               old_name="from_year",
                               new_name="year")
    ]

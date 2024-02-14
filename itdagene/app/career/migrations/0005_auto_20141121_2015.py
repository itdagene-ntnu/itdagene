from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("career", "0004_auto_20141121_2014")]

    operations = [
        migrations.RenameField(
            model_name="joblisting", old_name="year", new_name="from_year"
        )
    ]

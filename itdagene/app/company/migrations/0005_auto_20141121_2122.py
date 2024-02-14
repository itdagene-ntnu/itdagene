from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("company", "0004_auto_20141020_0000")]

    operations = [
        migrations.RemoveField(model_name="company", name="mp"),
        migrations.RemoveField(model_name="company", name="partner"),
    ]

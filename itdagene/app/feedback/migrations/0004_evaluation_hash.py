from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("feedback", "0003_auto_20141019_2216")]

    operations = [
        migrations.AddField(
            model_name="evaluation",
            name="hash",
            field=models.CharField(default="", max_length=100, verbose_name="Hash"),
            preserve_default=False,
        )
    ]

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("pages", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="page",
            name="language",
            field=models.CharField(
                choices=[("nb", "Norsk"), ("en", "English")], default="nb", max_length=3
            ),
        )
    ]

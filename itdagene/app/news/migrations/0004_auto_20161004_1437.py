from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("news", "0003_auto_20151109_1459")]

    operations = [
        migrations.AlterField(
            model_name="announcement",
            name="image",
            field=models.ImageField(
                blank=True, upload_to="announcements/", verbose_name="image"
            ),
        )
    ]

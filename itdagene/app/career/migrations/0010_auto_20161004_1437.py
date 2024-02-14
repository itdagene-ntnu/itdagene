from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("career", "0009_auto_20150922_1818")]

    operations = [
        migrations.AlterField(
            model_name="joblisting",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to="joblistings/", verbose_name="image"
            ),
        ),
        migrations.AlterField(
            model_name="joblisting",
            name="type",
            field=models.CharField(
                choices=[("si", "Summer internship"), ("pp", "Permanent position")],
                max_length=20,
                verbose_name="type",
            ),
        ),
    ]

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("events", "0002_auto_20141121_2310")]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="type",
            field=models.PositiveIntegerField(
                verbose_name="type",
                choices=[
                    (0, "Course"),
                    (1, "Company presentation"),
                    (2, "Banquet"),
                    (3, "Summer internship marathon"),
                    (4, "Baloon drop"),
                ],
            ),
            preserve_default=True,
        )
    ]

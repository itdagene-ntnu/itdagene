from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("experiences", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="experience",
            name="position",
            field=models.PositiveIntegerField(
                choices=[
                    (0, "Leder"),
                    (1, "Nestleder"),
                    (2, "Okonomi"),
                    (3, "Bedriftskontaktansvarlig"),
                    (4, "Logistikk"),
                    (5, "Markedsforing"),
                    (6, "Web"),
                    (7, "Bankett"),
                    (8, "Bedriftskontakt"),
                ],
                default=8,
                verbose_name="Position",
            ),
        )
    ]

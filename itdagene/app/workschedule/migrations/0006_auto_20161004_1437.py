from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("workschedule", "0005_auto_20150130_1925")]

    operations = [
        migrations.AlterField(
            model_name="worker",
            name="email",
            field=models.EmailField(blank=True, max_length=254, verbose_name="email"),
        ),
        migrations.AlterField(
            model_name="worker",
            name="t_shirt_size",
            field=models.IntegerField(
                choices=[
                    (1, "XS"),
                    (2, "S"),
                    (3, "M"),
                    (4, "L"),
                    (5, "XL"),
                    (6, "XXL"),
                    (7, "XXXL"),
                    (8, "XXXXL"),
                ],
                default=0,
                verbose_name="t-shirt size",
            ),
        ),
    ]

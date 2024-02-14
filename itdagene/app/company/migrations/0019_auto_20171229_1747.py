from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("company", "0018_auto_20161004_1437")]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="waiting_for_package",
            field=models.ManyToManyField(
                blank=True,
                related_name="waiting_list",
                to="company.Package",
                verbose_name="waiting for package",
            ),
        )
    ]

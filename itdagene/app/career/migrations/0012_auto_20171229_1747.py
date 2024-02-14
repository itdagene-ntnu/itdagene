from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("career", "0011_merge_20171229_1651")]

    operations = [
        migrations.AlterField(
            model_name="joblisting",
            name="towns",
            field=models.ManyToManyField(
                blank=True, to="career.Town", verbose_name="town"
            ),
        )
    ]

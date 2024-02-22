from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("company", "0016_auto_20160315_1950")]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="payment_email",
            field=models.EmailField(
                max_length=75, verbose_name="payment email", blank=True
            ),
            preserve_default=True,
        )
    ]

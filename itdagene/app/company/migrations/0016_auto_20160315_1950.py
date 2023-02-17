from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("company", "0015_auto_20160315_1949")]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="payment_email",
            field=models.CharField(max_length=100,
                                   verbose_name="payment email",
                                   blank=True),
            preserve_default=True,
        )
    ]

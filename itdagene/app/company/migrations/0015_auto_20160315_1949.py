from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0014_company_pamyent_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='pamyent_email',
            new_name='payment_email',
        ),
    ]

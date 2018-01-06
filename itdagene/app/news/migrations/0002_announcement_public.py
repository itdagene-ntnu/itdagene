from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('news', '0001_initial'), ]

    operations = [
        migrations.AddField(model_name='announcement',
                            name='public',
                            field=models.BooleanField(default=False,
                                                      verbose_name='public'),
                            preserve_default=True, ),
    ]

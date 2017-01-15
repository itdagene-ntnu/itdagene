from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('core', '0002_user_phone'), ]

    operations = [
        migrations.AddField(model_name='user',
                            name='photo',
                            field=models.ImageField(null=True,
                                                    upload_to=b'photos/users/',
                                                    blank=True),
                            preserve_default=True, ),
    ]

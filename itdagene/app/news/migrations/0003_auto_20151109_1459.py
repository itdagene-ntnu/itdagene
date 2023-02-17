from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("news", "0002_announcement_public")]

    operations = [
        migrations.AlterField(
            model_name="announcement",
            name="image",
            field=models.ImageField(upload_to="announcements/",
                                    verbose_name="image",
                                    blank=True),
            preserve_default=True,
        )
    ]

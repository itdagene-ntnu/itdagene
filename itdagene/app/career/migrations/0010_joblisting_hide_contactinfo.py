# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("career", "0009_auto_20150922_1818")]

    operations = [
        migrations.AddField(
            model_name="joblisting",
            name="hide_contactinfo",
            field=models.BooleanField(default=False,
                                      verbose_name="Hide contact info"),
            preserve_default=True,
        )
    ]

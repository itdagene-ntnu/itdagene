from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("core", "0018_delete_userproxy")]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="language",
            field=models.CharField(
                default="nb",
                max_length=3,
                verbose_name="Language",
                choices=[("nb", "Norsk"), ("en", "English")],
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="photo",
            field=models.ImageField(
                upload_to="photos/users/", null=True, verbose_name="Photo", blank=True
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="year",
            field=models.PositiveIntegerField(
                default=2015,
                max_length=3000,
                blank=True,
                help_text="Year the user was active.",
                null=True,
                verbose_name="Active Year",
            ),
        ),
    ]

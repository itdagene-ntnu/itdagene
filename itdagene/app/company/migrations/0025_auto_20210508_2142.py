# Generated by Django 2.2.13 on 2021-05-08 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("company", "0024_auto_20210117_0029"),
    ]

    operations = [
        migrations.RemoveField(model_name="company", name="is_collaborator",),
        migrations.AlterField(
            model_name="contract",
            name="banquet_tickets",
            field=models.PositiveIntegerField(
                default=1,
                help_text="Total, not additional",
                verbose_name="banquet tickets",
            ),
        ),
        migrations.AlterField(
            model_name="contract",
            name="interview_room",
            field=models.PositiveIntegerField(
                default=0,
                help_text="Total, not additional",
                verbose_name="interview room",
            ),
        ),
    ]

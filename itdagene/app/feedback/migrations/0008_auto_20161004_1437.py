# Generated by Django 1.10.2 on 2016-10-04 12:37
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("feedback", "0007_auto_20141124_0107")]

    operations = [
        migrations.AlterField(
            model_name="evaluation",
            name="company",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="company.Company",
                verbose_name="Company",
            ),
        ),
        migrations.AlterField(
            model_name="evaluation",
            name="preference",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="core.Preference",
                verbose_name="Preference",
            ),
        ),
        migrations.AlterField(
            model_name="issue",
            name="app",
            field=models.CharField(
                choices=[
                    ("all", "All"),
                    ("admin", "Admin"),
                    ("company", "BDB"),
                    ("career", "Career"),
                    ("core", "Core"),
                    ("events", "Events"),
                    ("feedback", "Feedback"),
                    ("frontpage", "Frontpage"),
                    ("logistics", "Logistics"),
                    ("mail", "Mail"),
                    ("meetings", "Meetings"),
                    ("news", "News"),
                    ("notifications", "Notifications"),
                    ("pages", "Pages"),
                    ("profiles", "Profiles"),
                    ("todo", "Todo"),
                    ("venue", "Venue"),
                    ("workschedule", "Workschedule"),
                ],
                max_length=50,
                verbose_name="app",
            ),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("feedback", "0007_auto_20141124_0107")]

    operations = [
        migrations.RemoveField(model_name="evaluation", name="opening_hours"),
        migrations.RemoveField(model_name="evaluation", name="other"),
        migrations.AddField(
            model_name="evaluation",
            name="communication_rating",
            field=models.IntegerField(
                default=0,
                verbose_name="What do you think about the communication and information given in advance of the event?",
                choices=[
                    (0, "Did not use"),
                    (1, "1: Very bad"),
                    (2, "2: Bad"),
                    (3, "3: Not bad or good"),
                    (4, "4: Good"),
                    (5, "5: Very good"),
                ],
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="evaluation",
            name="has_banquet",
            field=models.BooleanField(
                default=False, verbose_name="Were you at the banquet?"
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="evaluation",
            name="improvement",
            field=models.TextField(
                verbose_name="What could have been done better? Something else you want to comment?",
                blank=True,
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="evaluation",
            name="internship_marathon_improvement",
            field=models.TextField(
                verbose_name="What could have been done better at the internship marathon?",
                blank=True,
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="evaluation",
            name="internship_marathon_rating",
            field=models.IntegerField(
                default=0,
                verbose_name="How did the internship marathon go?",
                choices=[
                    (0, "Did not use"),
                    (1, "1: Very bad"),
                    (2, "2: Bad"),
                    (3, "3: Not bad or good"),
                    (4, "4: Good"),
                    (5, "5: Very good"),
                ],
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="evaluation",
            name="interview_location_improvement",
            field=models.TextField(
                verbose_name="What could have been done better at the interview room?",
                blank=True,
            ),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name="evaluation",
            name="visitors_rating",
            field=models.IntegerField(
                default=0,
                verbose_name="How satisfied are you with the number of people that visited your stand?",
                choices=[
                    (0, "Did not use"),
                    (1, "1: Very bad"),
                    (2, "2: Bad"),
                    (3, "3: Not bad or good"),
                    (4, "4: Good"),
                    (5, "5: Very good"),
                ],
            ),
            preserve_default=True,
        ),
    ]

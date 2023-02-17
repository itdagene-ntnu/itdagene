from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("company", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("career", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="town",
            name="creator",
            field=models.ForeignKey(
                related_name="town_creator",
                editable=False,
                on_delete=models.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="town",
            name="saved_by",
            field=models.ForeignKey(
                related_name="town_saved_by",
                on_delete=models.CASCADE,
                editable=False,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="joblisting",
            name="company",
            field=models.ForeignKey(
                related_name="joblistings",
                on_delete=models.CASCADE,
                verbose_name="company",
                to="company.Company",
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="joblisting",
            name="contact",
            field=models.ForeignKey(
                verbose_name="contact",
                on_delete=models.SET_NULL,
                blank=True,
                to="company.CompanyContact",
                null=True,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="joblisting",
            name="creator",
            field=models.ForeignKey(
                related_name="joblisting_creator",
                editable=False,
                on_delete=models.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="joblisting",
            name="saved_by",
            field=models.ForeignKey(
                related_name="joblisting_saved_by",
                on_delete=models.CASCADE,
                editable=False,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name="joblisting",
            name="towns",
            field=models.ManyToManyField(
                to="career.Town", null=True, verbose_name="town", blank=True
            ),
            preserve_default=True,
        ),
    ]

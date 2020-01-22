# Generated by Django 2.1.11 on 2020-01-19 20:41

from django.db import migrations
from django.utils.text import slugify


def gen_slug(apps, schema_editor):
    Joblisting = apps.get_model("career", "Joblisting")
    for joblisting in Joblisting.objects.all():
        joblisting.slug = slugify(
            f"{joblisting.company.name} {joblisting.date_created.strftime('%Y-%m-%d')}"
        )
        joblisting.save()


class Migration(migrations.Migration):

    dependencies = [("career", "0017_joblisting_slug")]

    operations = [
        migrations.RunPython(gen_slug, reverse_code=migrations.RunPython.noop)
    ]

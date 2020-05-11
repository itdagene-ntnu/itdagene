# Generated by Django 2.1.11 on 2020-01-21 14:38

from django.db import migrations, models
from django.utils.text import slugify


def fix_slug(apps, schema_editor):
    Joblisting = apps.get_model("career", "Joblisting")
    for joblisting in Joblisting.objects.all():
        joblisting.slug = slugify(f"{joblisting.id} {joblisting.title}")
        joblisting.save()


class Migration(migrations.Migration):

    dependencies = [("career", "0018_gen_slug")]

    operations = [
        migrations.AlterField(
            model_name="joblisting",
            name="slug",
            field=models.SlugField(editable=True, unique=False, max_length=150),
        ),
        migrations.RunPython(fix_slug, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name="joblisting",
            name="slug",
            field=models.SlugField(editable=False, unique=True, max_length=150),
        ),
    ]
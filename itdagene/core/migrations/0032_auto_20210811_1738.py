from django.db import migrations
from django.db.migrations import AddField, AlterField
from django.db.models import BooleanField, TextField, URLField


class Migration(migrations.Migration):
    dependencies = [("core", "0031_auto_20210508_2206")]

    operations = [
        AddField(
            model_name="preference",
            name="hsp_intro",
            field=TextField(
                blank=True,
                default="",
                help_text=(
                    "Introduction of main collaborator to be displayed above "
                    "video on front page"
                ),
            ),
        ),
        AddField(
            model_name="preference",
            name="hsp_poster",
            field=URLField(
                blank=True,
                help_text="URL to the image to display before video is played",
                null=True,
            ),
        ),
        AddField(
            model_name="preference",
            name="hsp_video",
            field=URLField(
                blank=True,
                help_text="URL to the video introduction of main collaborator",
                null=True,
            ),
        ),
        AlterField(
            model_name="preference",
            name="view_hsp",
            field=BooleanField(
                default=False,
                help_text="Should the main collaborator be displayed on the front page?<br/><br/>",
                verbose_name="view main collaborator",
            ),
        ),
    ]

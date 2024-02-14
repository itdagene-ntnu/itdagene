from django.db import migrations
from django.db.migrations import AlterField
from django.db.models import BooleanField, TextField, URLField


class Migration(migrations.Migration):
    dependencies = [("core", "0033_merge_20210822_1425")]

    operations = [
        AlterField(
            model_name="preference",
            name="hsp_intro",
            field=TextField(
                blank=True,
                default="",
                help_text=(
                    "Introduction of main collaborator to be displayed above "
                    "video on front page"
                ),
                verbose_name="Main collaborator introduction",
            ),
        ),
        AlterField(
            model_name="preference",
            name="hsp_poster",
            field=URLField(
                blank=True,
                help_text="URL to the image to display before video is played",
                null=True,
                verbose_name="Main collaborator poster URL",
            ),
        ),
        AlterField(
            model_name="preference",
            name="hsp_video",
            field=URLField(
                blank=True,
                help_text="URL to the video introduction of main collaborator",
                null=True,
                verbose_name="Main collaborator video URL",
            ),
        ),
        AlterField(
            model_name="preference",
            name="view_hsp",
            field=BooleanField(
                default=False,
                help_text="Should the main collaborator be displayed on the front page?",
                verbose_name="view main collaborator",
            ),
        ),
    ]

from django.conf import settings
from django.db import migrations
from django.db.migrations import AddField, AlterUniqueTogether, RemoveField
from django.db.models import ManyToManyField


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("notifications", "0007_auto_20150130_1925"),
    ]

    operations = [
        RemoveField(model_name="notification", name="read"),
        RemoveField(model_name="notification", name="user"),
        AddField(
            model_name="notification",
            name="users",
            field=ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name="users"),
            preserve_default=True,
        ),
        AlterUniqueTogether(
            name="subscription",
            unique_together={("content_type", "object_id")},
        ),
    ]

from django.contrib.auth.models import UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import migrations
from django.db.migrations import AlterField, AlterModelManagers
from django.db.models import (
    CharField,
    DateTimeField,
    EmailField,
    ImageField,
    ManyToManyField,
)


class Migration(migrations.Migration):
    dependencies = [("core", "0022_auto_20160215_1141")]

    operations = [
        AlterModelManagers(
            name="user",
            managers=[("objects", UserManager())],
        ),
        AlterField(
            model_name="user",
            name="email",
            field=EmailField(blank=True, max_length=254, verbose_name="email address"),
        ),
        AlterField(
            model_name="user",
            name="groups",
            field=ManyToManyField(
                blank=True,
                help_text=(
                    "The groups this user belongs to. A user will get all "
                    "permissions granted to each of their groups."
                ),
                related_name="user_set",
                related_query_name="user",
                to="auth.Group",
                verbose_name="groups",
            ),
        ),
        AlterField(
            model_name="user",
            name="language",
            field=CharField(
                choices=[("nb", "Norsk"), ("en", "English")],
                default="nb",
                max_length=3,
                verbose_name="Language",
            ),
        ),
        AlterField(
            model_name="user",
            name="last_login",
            field=DateTimeField(blank=True, null=True, verbose_name="last login"),
        ),
        AlterField(
            model_name="user",
            name="photo",
            field=ImageField(
                blank=True,
                null=True,
                upload_to="photos/users/",
                verbose_name="Photo",
            ),
        ),
        AlterField(
            model_name="user",
            name="username",
            field=CharField(
                error_messages={"unique": "A user with that username already exists."},
                help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                max_length=150,
                unique=True,
                validators=[UnicodeUsernameValidator()],
                verbose_name="username",
            ),
        ),
    ]

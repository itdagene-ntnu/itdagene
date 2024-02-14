from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("todo", "0003_remove_todo_title")]

    operations = [
        migrations.AlterField(
            model_name="todo",
            name="description",
            field=models.TextField(verbose_name="description"),
        )
    ]

from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('notifications', '0005_auto_20140929_0353'), ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(auto_now=True,
                                       verbose_name='date'), ),
        migrations.AlterField(
            model_name='notification',
            name='message',
            field=models.TextField(verbose_name='message'), ),
        migrations.AlterField(
            model_name='notification',
            name='priority',
            field=models.PositiveIntegerField(
                default=1,
                verbose_name='priority',
                choices=[(0, b'Low'), (1, b'Medium'), (2, b'High')]), ),
        migrations.AlterField(
            model_name='notification',
            name='send_mail',
            field=models.BooleanField(default=True,
                                      verbose_name='send mail'), ),
        migrations.AlterField(
            model_name='notification',
            name='sent_mail',
            field=models.BooleanField(default=False,
                                      verbose_name='sent mail'), ),
    ]

from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [('feedback', '0006_auto_20141124_0028'), ]

    operations = [migrations.AlterField(
        model_name='evaluation',
        name='course_improvement',
        field=models.TextField(verbose_name='Could the course be handled better?',
                               blank=True), ),
                  migrations.AlterField(
                      model_name='evaluation',
                      name='internship_marathon_improvement',
                      field=models.TextField(
                          verbose_name=
                          'What could have been done better at the kickstart?',
                          blank=True), ), ]

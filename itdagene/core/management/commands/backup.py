# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.conf import settings
import time

def safe_unicode(obj):
    string = str(obj)
    return string.decode('latin1').encode('utf8')

class Command (BaseCommand):

    option_list = BaseCommand.option_list

    requires_model_validation = False
    help=''
    def handle(self, *args, **options):
        import os
        with open('/django-sites/db-pw/prod', 'rb') as f:
            db_password = f.readline()
        db_password = db_password.replace("\n","").strip()

        base_path = os.path.dirname(os.path.dirname(settings.ROOTPATH))
        db_name = 'django-prod'
        username = 'django-prod'
        password = db_password
        path = os.path.join(base_path, "tmp-backups/itdagene-prod-" + time.strftime('%y-%m-%d-%H-%M') + '.sql.gz')
        command = 'pg_dump -U ' + username + ' ' + db_name + ' | gzip -c -9" > ' + path
        pipe = os.popen(command)
        pipe.write(password)
        pipe.write("\n")
        if os.path.getsize(path) > 0: return path
        else: return None
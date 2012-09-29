# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.conf import settings

def safe_unicode(obj):
    string = str(obj)
    return string.decode('latin1').encode('utf8')

class Command (BaseCommand):

    option_list = BaseCommand.option_list
    
    requires_model_validation = False
    help='Run the migration'
    def handle(self, *args, **options):
        import os
        os.system('git pull')
        os.system('bin/django migrate')
        path = settings.ROOTPATH.replace('/project','')
        ini_file = os.path.basename(path) + '.ini'
        os.system('touch ../uwsgi/' + ini_file)
        print ini_file + ' touched'
        print '---------------------'
        print 'The site was updated'

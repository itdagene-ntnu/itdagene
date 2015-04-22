# -*- coding: utf-8 -*-
import json
import os
import time

from django.conf import settings
from django.core.management.base import BaseCommand

from itdagene.app.workschedule.models import Worker


def safe_unicode(obj):
    string = str(obj)
    return string.decode('latin1').encode('utf8')

class Command (BaseCommand):

    option_list = BaseCommand.option_list

    requires_model_validation = False
    help=''
    def handle(self, *args, **options):
        path = args[0]
        if not os.path.exists(path):
            print "First argument should be the path to the file with worker info"
            return

        json_data=open(path)
        data = json.load(json_data)
        count = 0

        for worker in data:
            w = Worker(
                phone=int(worker['tlf']),
                username=worker['username'],
                email="%s@stud.ntnu.no" % worker['username'],

            )
            if 'name' in worker:
                w.name = worker['name']
            else:
                w.name="%s %s" % (worker['firstname'], worker['lastname']),

            try:
                w.t_shirt_size=int(worker['storrelse'])
            except ValueError:
                str = worker['storrelse'].upper()
                if str == 'XS':
                    w.t_shirt_size = 1
                elif str == 'S':
                    w.t_shirt_size = 2
                elif str == 'M':
                    w.t_shirt_size = 3
                elif str == 'L':
                    w.t_shirt_size = 4
                elif str == 'XL':
                    w.t_shirt_size = 5
                elif str == 'XXL':
                    w.t_shirt_size = 6
                elif str == 'XXXL':
                    w.t_shirt_size = 7
                elif str == 'XXXXL':
                    w.t_shirt_size = 8

            w.save()
            count += 1

        print "Added %d workers" % count

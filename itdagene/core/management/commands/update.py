# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.conf import settings

from rest_framework import serializers
from StringIO import StringIO
from rest_framework.parsers import JSONParser
from itdagene.core.models import User


def safe_unicode(obj):
    string = str(obj)
    return string.decode('latin1').encode('utf8')


class RestoreSerializer(serializers.Serializer):
    pass


class Command (BaseCommand):

    option_list = BaseCommand.option_list

    requires_model_validation = False
    help = 'Run the migration'

    def handle(self, *args, **options):

        f = open('backup.json', 'r')
        lines = f.readlines()
        line = lines[0]

        stream = StringIO(line)
        data = JSONParser().parse(stream)

        for obj in data:
            if obj['first_name'] == '' or obj['first_name'] == 'anonymous':
                continue
            if obj['year'] == 2015:
                continue

            User.objects.create(
                username=obj['username'],
                last_login=obj['last_login'],
                first_name=obj['first_name'],
                last_name=obj['last_name'],
                email=obj['email'],
                is_active=True,
                date_joined=obj['date_joined'],
                phone=obj['phone']
                )

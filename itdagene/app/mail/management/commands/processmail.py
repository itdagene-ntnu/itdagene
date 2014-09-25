from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import email
import os
import sys

class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('--test-option', action='store_false', dest='use_test', default=False,
            help='Does test things'),
    )
    requires_model_validation = True
    help = "Processes a mail"
    args = '<recipients> <sender>'

    def handle(self, sender, *recipients, **options):
        msg = email.message_from_file(sys.stdin)
        for recipient in recipients:
            print(msg, sender, recipient)
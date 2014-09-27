# -*- coding: utf-8 -*-
from django.conf import settings
from itdagene.app.mail.models import MailMapping
from copy import copy
from django.core import mail as djangomail
import subprocess
from django.template.loader import render_to_string
from email.message import Message
from email.mime.text import MIMEText



def fix_headers(message, headers):
    for key, val in headers.iteritems():
        if key in message:
            message.replace_header(key, val)
        else:
            message[key] = val


def sendmail(args, msg):
    if settings.EMAIL_BACKEND=='django.core.mail.backends.locmem.EmailBackend':
        msg['X-args']=unicode(args[1:])

        if not hasattr(msg, 'message'):
            msg.message = lambda: None

        djangomail.get_connection(fail_silently=False).send_messages((msg,))
    else:
        print(args)
        process = subprocess.Popen(args,stdin=subprocess.PIPE, close_fds=True)
        process.stdin.write(msg.as_string())
        process.stdin.close()


def send_message(message, addresses, sender):
    common_arguments = [settings.MAIL_SENDMAIL_EXECUTABLE, '-G', '-i', '-f', sender]
    for i in xrange(0,len(addresses),settings.MAIL_BATCH_LENGTH):
        current_addresses = addresses[i : i+settings.MAIL_BATCH_LENGTH]
        current_arguments = copy(common_arguments)
        current_arguments.extend(current_addresses)
        sendmail(current_arguments, message)


def handle_mail(msg, sender, recipient):
    prefix, domain = recipient.split('@')
    prefix, domain = prefix.lower(), domain.lower()


    if domain in settings.MAIL_DESTINATION:
        recipients = MailMapping.get_destinations_and_headers(prefix, domain)

        if len(recipients.keys()) > 0:
            for recipient in recipients.keys():
                if '@' in recipient and len(recipient) > 3:
                    # Send message to recipient
                    headers = recipients[recipient]
                    current_message = copy(msg)
                    fix_headers(current_message, headers)
                    send_message(current_message, [ recipient ], settings.SERVER_EMAIL)
        else:
            mail_contents = render_to_string('mail/backend/bounce.html', {'sender': sender, 'recipient': recipient, 'prefix': prefix, 'domain': domain})
            message = Message()
            message.set_payload(str(MIMEText(mail_contents.encode('iso-8859-1'))))
            message['Subject'] = 'Mail address does not exist'
            message['Sender'] = settings.SERVER_EMAIL
            message['To'] = sender
            message['X-bounce'] = 'True'
            send_message(message, [ sender ], settings.SERVER_EMAIL)
# -*- coding: utf-8 -*-
from django.conf import settings
from django.core import mail as djangomail
import subprocess
from django.template.loader import render_to_string
from email.message import Message
from email.mime.text import MIMEText
from copy import copy
from itdagene.app.mail.models import MailMapping
from django.utils.translation import ugettext_lazy as _
from django.core.mail import mail_admins


def fix_headers(message, headers):
    """Replace or set headers in a message working around some peculiarities in the email-module"""
    for key, val in headers.iteritems():
        if key  in message:
            message.replace_header(key, val)
        else:
            message[key] = val

def sendmail(args, msg):
    """ Do call sendmail with args and message
    Security breack if not the first argument is whitelisted
    and the resulting program uses the rest of the arguments wisely
    """

    process = subprocess.Popen(args,stdin=subprocess.PIPE, close_fds=True)
    process.stdin.write(msg.as_string())
    process.stdin.close()


def send_message(message, addresses, sender):
    """Send message via sendmail; splitting up in MAIL_BATCH_LENGTH batches"""
    common_arguments = [settings.MAIL_SENDMAIL_EXECUTABLE, '-G', '-i', '-f', sender]
    for i in xrange(0,len(addresses),settings.MAIL_BATCH_LENGTH):
        current_addresses = addresses[i : i+settings.MAIL_BATCH_LENGTH]
        current_arguments = copy(common_arguments)
        current_arguments.extend(current_addresses)
        sendmail(current_arguments, message)

def handle_mail(msg, sender, recipient):
    prefix, domain = recipient.split('@')
    prefix = prefix.lower()
    try:
        if domain in settings.MAIL_DESTINATION:

            aliases = MailMapping.get_destinations_and_headers(prefix, domain)

            if len(aliases['addresses']) == 0 and not sender == recipient:

                #send bounce
                mail_contents = render_to_string('mail/backend/bounce.html', {
                                                 'sender': sender,
                                                 'recipient': recipient,
                                                 'prefix': prefix,
                                                 'domain': domain})
                message = Message()
                message.set_payload(str(MIMEText(mail_contents.encode('iso-8859-1'))))
                message['Subject'] = _('Mail address does not exist')
                message['Sender'] = '%s@%s' % ('bounce', settings.SITE['domain'])
                message['To'] = sender
                message['X-bounce'] = 'True'
                send_message(message, [sender], '%s@%s' % ('bounce', settings.SITE['domain']))

                for a in settings.ADMINS:
                    if sender == a[1]:
                        return

                mail_admins(_('Bounce Mail'), msg.as_string())

            elif not len(aliases['addresses']) == 0:
                current_message = copy(msg)
                fix_headers(current_message, aliases['headers'])
                send_message(current_message, aliases['addresses'], settings.SITE['email'])

    except Exception as ex:
        try:
            msg_data = msg.as_string()
        except TypeError as ex:
            msg_data = "TypeError:" + repr(ex)

        mail_contents = render_to_string('mail/backend/exception.html', {'ex': ex,
                                         'sender': sender,
                                         'recipient': recipient,
                                         'message': msg_data,
                                         'prefix': prefix,
                                         'domain': domain})
        #send to sender
        message = Message()
        message.set_payload(str(MIMEText(mail_contents.encode('iso-8859-1'))))
        message['Subject'] = _('Exception while sending mail')
        message['From'] = settings.SITE['email']
        message['To'] = sender
        message['X-bounce'] = 'True'
        send_message(message, [sender], settings.SITE['email'])

        for a in settings.ADMINS:
            if sender == a[1]:
                return

        mail_admins(_('Exception while sending mail'), mail_contents)

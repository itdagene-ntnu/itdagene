from django.template.loader import render_to_string
from django.core.mail import get_connection, EmailMultiAlternatives
from django.conf import settings
from django.utils.translation import ugettext as _
from itdagene.core.auth import generate_password


def send_email(recipients, subject, template, template_html, params, sender=settings.SERVER_EMAIL):

    params['site'] = settings.SITE

    mail_contents = render_to_string('mail/mail/%s' % (template, ), params)
    mail_contents_html = render_to_string('mail/mail/%s' % (template_html, ), params)

    connection = get_connection(fail_silently=True)

    messages = []
    for recipient in recipients:
        message = EmailMultiAlternatives(str(subject), mail_contents, sender, [recipient])
        message.attach_alternative(mail_contents_html, 'text/html')
        messages.append(message)

    return connection.send_messages(messages)


def users_send_welcome_email(user):
    new_password = generate_password()
    user.set_password(new_password)
    user.save()
    return send_email([user.email], '%s %s' % (_('Welcome to'), settings.SITE['name']), 'users/welcome_mail.txt', 'users/welcome_mail.html', { 'title': '%s %s' % (_('Welcome to'), settings.SITE['name']), 'user': user, 'password': new_password})
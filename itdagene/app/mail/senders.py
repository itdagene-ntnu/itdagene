from django.template.loader import render_to_string
from django.core.mail import get_connection, EmailMultiAlternatives
from django.conf import settings
from django.utils.translation import ugettext as _
from itdagene.core.auth import generate_password
from django.utils import translation
from itdagene.core.auth import get_current_user


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
    translation.activate(user.language)
    new_password = generate_password()
    user.set_password(new_password)
    user.save()
    result = send_email([user.email], '%s %s' % (_('Welcome to'), settings.SITE['name']), 'users/welcome_mail.txt', 'users/welcome_mail.html', { 'title': '%s %s' % (_('Welcome to'), settings.SITE['name']), 'user': user, 'password': new_password})
    if not get_current_user().is_anonymous():
        translation.activate(get_current_user().language)
    return result

def notifications_send_email(notification):
    translation.activate(notification.user.language)
    context = {
        'title': _('You have a new notification'),
        'notification': notification,
        'base_url': 'http://%s' % (settings.SITE['domain'])
    }
    template, template_html = 'notifications/notification_mail.txt', 'notifications/notification_mail.html'
    result = send_email([notification.user.email], _('You have a new notification'), template, template_html, context)
    if not get_current_user().is_anonymous():
        translation.activate(get_current_user().language)
    return result

def meeting_send_invite(users, meeting):
    for user in users:
        translation.activate(user.language)
        context = {
            'title': _('Meeting Invitation'),
            'meeting': meeting,
            'base_url': 'http://%s' % (settings.SITE['domain'], )
        }
        template, template_html = 'meetings/invite.txt', 'meetings/invite.html'
        result = send_email([user.email], _('Meeting Invite'), template, template_html, context)
        if not get_current_user().is_anonymous():
            translation.activate(get_current_user().language)
    return True
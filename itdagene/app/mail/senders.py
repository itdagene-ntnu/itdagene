from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.utils import formats, translation
from django.utils.translation import gettext_lazy as _

from itdagene.app.comments.models import Comment
from itdagene.core.auth import generate_password
from itdagene.core.notifications.models import Subscription


def send_email(
    recipients,
    subject: str,
    template: str,
    template_html: str,
    params: dict,
    sender: str = settings.SERVER_EMAIL,
):
    params["site"] = settings.SITE

    mail_contents = render_to_string(f"mail/{template}", params)
    mail_contents_html = render_to_string(f"mail/{template_html}", params)

    connection = get_connection(fail_silently=True)

    messages: list = []
    for recipient in recipients:
        message = EmailMultiAlternatives(subject, mail_contents, sender, [recipient])
        message.attach_alternative(mail_contents_html, "text/html")
        messages.append(message)

    return connection.send_messages(messages)


def users_send_welcome_email(user) -> None:
    with translation.override(user.language):
        new_password = generate_password()
        user.set_password(new_password)
        user.save()

        send_email(
            [user.email],
            f"{_('Welcome to')} {settings.SITE['name']}",
            "users/welcome_mail.txt",
            "users/welcome_mail.html",
            {"user": user, "password": new_password},
        )


def notifications_send_email(notification) -> None:
    for user in notification.users.all():
        if not user.mail_notification:
            continue

        with translation.override(user.language):
            context = {"notification": notification}

            template, template_html = (
                "notifications/notification_mail.txt",
                "notifications/notification_mail.html",
            )

            send_email(
                [user.email],
                _("New notification"),
                template,
                template_html,
                context,
            )


def meeting_send_invite(users, meeting) -> None:
    for user in users:
        with translation.override(user.language):
            context = {"meeting": meeting}
            template, template_html = (
                "meetings/invite.txt",
                "meetings/invite.html",
            )
            send_email(
                [user.email],
                _(f"Meeting Invite {meeting} {formats.date_format(meeting.date)}"),
                template,
                template_html,
                context,
            )


def send_comment_email(comment) -> None:
    attached_object = comment.object

    if attached_object:
        all_object_comments = Comment.objects.filter(
            object_id=comment.object_id, content_type=comment.content_type
        )

        def get_users(comment):
            return comment.user

        users = list(map(get_users, all_object_comments))

        try:
            subscription = Subscription.objects.get(
                content_type=ContentType.objects.get_for_model(attached_object),
                object_id=attached_object.id,
            )
            users += subscription.subscribers.all()
        except Subscription.DoesNotExist:
            pass

        users = list(set(users))

        for user in users:
            if not user.mail_notification:
                continue

            with translation.override(user.language):
                context = {"comment": comment}

                template, template_html = "comment/new.txt", "comment/new.html"

                send_email(
                    [user.email],
                    _(f"New comment on {comment.object}"),
                    template,
                    template_html,
                    context,
                )

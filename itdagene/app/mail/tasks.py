from django.conf import settings
from django.core.mail import mail_admins

from itdagene.app.mail.senders import meeting_send_invite as msi
from itdagene.app.mail.senders import notifications_send_email as nse
from itdagene.app.mail.senders import send_comment_email as ce
from itdagene.celery import app


@app.task(bind=True)
def meeting_send_invite(self, users, meeting) -> None:
    msi(users, meeting)


@app.task(bind=True)
def send_notification_message(self, notification) -> None:
    nse(notification)


@app.task(bind=True)
def send_comment_email(self, comment) -> None:
    ce(comment)


@app.task(bind=True)
def send_admin_mail(self, log_item) -> None:
    mail_admins(
        f"Log: {log_item}",
        f"{log_item}\n Read more at http://{settings.SITE['domain']}"
        f"{log_item.content_object.get_absolute_url()}",
    )

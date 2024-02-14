import os

import celery
from raven import Client
from raven.contrib.celery import register_logger_signal, register_signal


class Celery(celery.Celery):
    def on_configure(self) -> None:
        client = Client()

        # register a custom filter to filter out duplicate logs
        register_logger_signal(client)

        # hook into the Celery error handler
        register_signal(client)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "itdagene.settings")

app = Celery("itdagene")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self) -> None:
    print(f"Request: {self.request!r}")

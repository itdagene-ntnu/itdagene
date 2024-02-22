from django.contrib import admin

from itdagene.app.events.models import Event, Ticket


admin.site.register(Event)
admin.site.register(Ticket)

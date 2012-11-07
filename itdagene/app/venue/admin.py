from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from itdagene.app.venue.models import Stand

class StandAdmin(ModelAdmin):
    pass
admin.site.register(Stand, StandAdmin)
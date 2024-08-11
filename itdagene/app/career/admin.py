from django.contrib import admin
from django.contrib.admin import ModelAdmin

from itdagene.app.career.models import Joblisting, Town


admin.site.register(Town)


class JoblistingAdmin(ModelAdmin):
    list_display = ("title", "company")


admin.site.register(Joblisting, JoblistingAdmin)

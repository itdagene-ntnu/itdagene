from itdagene.app.career.models import Joblisting, Town
from django.contrib import admin

admin.site.register(Town)

class JoblistingAdmin(admin.ModelAdmin):
    list_display = ('title', 'company')

admin.site.register(Joblisting, JoblistingAdmin)

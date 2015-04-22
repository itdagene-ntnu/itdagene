from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from itdagene.app.experiences.models import Experience


class ExperienceAdmin(ModelAdmin):
    list_display = ('position', 'year', 'last_updated')
    list_filter = ('position', 'year')


admin.site.register(Experience, ExperienceAdmin)

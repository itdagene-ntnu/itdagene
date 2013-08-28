from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from itdagene.core.profiles.models import Profile, BoardPosition

class BoardPositionAdmin (ModelAdmin):
    list_display = ('title', 'email')

admin.site.register(BoardPosition, BoardPositionAdmin)

class ProfileAdmin (ModelAdmin):
    list_display = ('user', 'type', 'phone', 'language')
    list_filter = ('type', 'position', 'year')

admin.site.register(Profile, ProfileAdmin)
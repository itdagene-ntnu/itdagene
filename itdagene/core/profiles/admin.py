from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from itdagene.core.models import User
from itdagene.core.profiles.models import Profile, BoardPosition


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profiles'
    fk_name = 'user'


class BoardPositionAdmin (ModelAdmin):
    list_display = ('title', 'email')


class NewUserAdmin(UserAdmin):
    inlines = (ProfileInline, )


admin.site.register(BoardPosition, BoardPositionAdmin)

admin.site.unregister(User)
admin.site.register(User, NewUserAdmin)
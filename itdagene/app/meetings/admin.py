from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from itdagene.app.meetings.models import Meeting, Penalty, ReplyMeeting


class ReplyMeetingInline (admin.TabularInline):
    model = ReplyMeeting

class MeetingAdmin (ModelAdmin):
    list_display = ('date', 'start_time', 'end_time')
    inlines = [ReplyMeetingInline]
admin.site.register(Meeting, MeetingAdmin)

class ReplyMeetingAdmin (ModelAdmin):
    list_display = ('user', 'meeting')
admin.site.register(ReplyMeeting, ReplyMeetingAdmin)

class PenaltyAdmin (ModelAdmin):
    list_display = ('user', 'bottles', 'type', 'meeting')
admin.site.register(Penalty, PenaltyAdmin)

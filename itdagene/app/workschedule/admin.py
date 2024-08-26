from django.contrib import admin
from django.contrib.admin import TabularInline
from django.contrib.admin.options import ModelAdmin

from itdagene.app.workschedule.models import Worker, WorkerInSchedule, WorkSchedule


class WorkerInScheduleInline(TabularInline):
    model = WorkerInSchedule
    extra = 0


class WorkerAdmin(ModelAdmin):
    list_display = ("name", "email", "phone")
    list_filter = ("t_shirt_size",)
    inlines = [WorkerInScheduleInline]


admin.site.register(Worker, WorkerAdmin)


class WorkScheduleAdmin(ModelAdmin):
    list_display = ("title", "date", "start_time", "end_time", "workers")
    date_hierarchy = "date"
    inlines = [WorkerInScheduleInline]


admin.site.register(WorkSchedule, WorkScheduleAdmin)

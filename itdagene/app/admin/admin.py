from django.contrib import admin
from app.feedback.models import Issue, Evaluation, EvaluationHash

def company(obj):
    return str(obj.hash.company)

def pref(obj):
    return str(obj.hash.pref)


class EvaluationAdmin (admin.ModelAdmin):
    list_display = (company, pref)
    readonly_fields = (
        'hash',
        'internship_marathon_rating',
        'internship_marathon_improvement',
        'course_rating',
        'course_improvement',
        'visitors_rating',
        'has_interview_location',
        'interview_location_rating',
        'interview_location_improvement',
        'has_banquet',
        'banquet_rating',
        'banquet_improvement',
        'opening_hours',
        'improvement',
        'other',
        'want_to_come_back',
    )




admin.site.register(Issue)
admin.site.register(Evaluation, EvaluationAdmin)
admin.site.register(EvaluationHash)
from django.contrib import admin

from itdagene.app.feedback.models import Evaluation, EvaluationHash, Issue

admin.site.register(Issue)
admin.site.register(Evaluation)
admin.site.register(EvaluationHash)

from django.contrib import admin
from itdagene.app.feedback.models import Issue, Evaluation, EvaluationHash

admin.site.register(Issue)
admin.site.register(Evaluation)
admin.site.register(EvaluationHash)
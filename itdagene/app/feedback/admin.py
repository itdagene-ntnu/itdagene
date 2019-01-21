from django.contrib import admin
from itdagene.app.feedback.models import Evaluation, Issue

admin.site.register(Issue)
admin.site.register(Evaluation)

from django.http import HttpResponsePermanentRedirect
from django.urls import re_path

from itdagene.app.feedback.views import evalutions, issues

urlpatterns = [
    re_path(r'^$', lambda r: HttpResponsePermanentRedirect('/feedback/issues/')),
    re_path(r'^report/$', evalutions.report, name='itdagene.app.feedback.views.evalutions.report'),
    re_path(
        r'^report/(?P<year>\d{4})/$', evalutions.report,
        name='itdagene.app.feedback.views.evalutions.report'
    ),
    re_path(r'^evaluate/(?P<hash>.+)/$', evalutions.handle_evaluation),
    re_path(r'^issues/$', issues.list, name='itdagene.app.feedback.views.issues.list'),
    re_path(
        r'^issues/solved/$', issues.solved_list,
        name='itdagene.app.feedback.views.issues.solved_list'
    ),
    re_path(
        r'^issues/mine/$', issues.my_issues, name='itdagene.app.feedback.views.issues.my_issues'
    ),
    re_path(r'^issues/add$', issues.add, name='itdagene.app.feedback.views.issues.add'),
    re_path(r'^issues/(?P<id>\d+)/$', issues.view, name='itdagene.app.feedback.views.issues.view'),
    re_path(
        r'^issues/(?P<id>\d+)/edit$', issues.edit, name='itdagene.app.feedback.views.issues.edit'
    ),
    re_path(
        r'^issues/(?P<id>\d+)/solved$', issues.solved,
        name='itdagene.app.feedback.views.issues.solved'
    ),
]

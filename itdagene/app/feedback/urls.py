from django.conf.urls import url
from django.http import HttpResponsePermanentRedirect

from itdagene.app.feedback.views import evalutions, issues

urlpatterns = [
    url(r'^$', lambda r: HttpResponsePermanentRedirect('/feedback/issues/')),
    url(r'^report/$', evalutions.report, name='itdagene.app.feedback.views.evalutions.report'),
    url(
        r'^report/(?P<year>\d{4})/$', evalutions.report,
        name='itdagene.app.feedback.views.evalutions.report'
    ),
    url(r'^evaluate/(?P<hash>.+)/$', evalutions.handle_evaluation),
    url(r'^issues/$', issues.list, name='itdagene.app.feedback.views.issues.list'),
    url(
        r'^issues/solved/$', issues.solved_list,
        name='itdagene.app.feedback.views.issues.solved_list'
    ),
    url(r'^issues/mine/$', issues.my_issues, name='itdagene.app.feedback.views.issues.my_issues'),
    url(r'^issues/add$', issues.add, name='itdagene.app.feedback.views.issues.add'),
    url(r'^issues/(?P<id>\d+)/$', issues.view, name='itdagene.app.feedback.views.issues.view'),
    url(r'^issues/(?P<id>\d+)/edit$', issues.edit, name='itdagene.app.feedback.views.issues.edit'),
    url(
        r'^issues/(?P<id>\d+)/solved$', issues.solved,
        name='itdagene.app.feedback.views.issues.solved'
    ),
]

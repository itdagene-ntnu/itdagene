from django.conf.urls import url
from django.http import HttpResponsePermanentRedirect

urlpatterns = [
    url(r'^$', lambda r: HttpResponsePermanentRedirect('/feedback/issues/')),
    url(r'^report/$', 'itdagene.app.feedback.views.evalutions.report'),
    url(r'^report/(?P<year>\d{4})/$', 'itdagene.app.feedback.views.evalutions.report',
        name='report'),
    url(r'^evaluate/(?P<hash>.+)/$', 'itdagene.app.feedback.views.evalutions.handle_evaluation'),

    url(r'^issues/$', 'itdagene.app.feedback.views.issues.list', name='issues'),
    url(r'^issues/solved/$', 'itdagene.app.feedback.views.issues.solved_list'),
    url(r'^issues/mine/$', 'itdagene.app.feedback.views.issues.my_issues'),
    url(r'^issues/add$', 'itdagene.app.feedback.views.issues.add'),
    url(r'^issues/(?P<id>\d+)/$', 'itdagene.app.feedback.views.issues.view'),
    url(r'^issues/(?P<id>\d+)/edit$', 'itdagene.app.feedback.views.issues.edit'),
    url(r'^issues/(?P<id>\d+)/solved$', 'itdagene.app.feedback.views.issues.solved'),
]

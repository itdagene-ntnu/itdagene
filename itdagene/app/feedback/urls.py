from django.conf.urls import url, patterns
from django.http import HttpResponsePermanentRedirect

urlpatterns = patterns('itdagene.app.feedback.views',
    url(r'^$', lambda r: HttpResponsePermanentRedirect('/feedback/issues/')),
    url(r'^report/$', 'evalutions.report'),
    url(r'^report/(?P<year>\d{4})/$', 'evalutions.report', name='report'),
)

urlpatterns += patterns('itdagene.app.feedback.views.issues',
            url(r'^issues/$', 'list', name='issues'),
            url(r'^issues/solved/$', 'list', {'solved': True}, name='solved_issues'),
            url(r'^issues/mine/$', 'my_issues'),
            url(r'^issues/add$', 'edit'),
            url(r'^issues/(?P<id>\d+)/$', 'view'),
            url(r'^issues/(?P<id>\d+)/edit$', 'edit'),
            url(r'^issues/(?P<id>\d+)/solved$', 'solved'),
)

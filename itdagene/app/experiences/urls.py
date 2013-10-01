from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('itdagene.app.experiences.views',
            url(r'^$', 'list'),
            url(r'^add$', 'add'),
            url(r'^(?P<id>\d+)/$', 'view'),
            url(r'^(?P<id>\d+)/edit$', 'edit'),
)
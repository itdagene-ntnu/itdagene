from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('itdagene.app.pages.views',
    (r'^$', 'view_page'),
    url(r'^pages/$', 'admin', name='pages'),
    (r'^pages/add$', 'add'),
    (r'^(?P<lang_code>[a-z][a-z])/(?P<slug>.*)/edit/$', 'edit'),
    (r'^(?P<lang_code>[a-z][a-z])/(?P<slug>.*)/$', 'view_page'),
    (r'^(?P<slug>.*)/edit/$', 'edit'),
    (r'^(?P<slug>.*)/$', 'view_page'),
)

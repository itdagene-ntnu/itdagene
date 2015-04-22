from django.conf.urls import url

urlpatterns = [
    url(r'^pages/$', 'itdagene.app.pages.views.admin', name='pages'),
    url(r'^pages/add/$', 'itdagene.app.pages.views.add'),
    url(r'^$', 'itdagene.app.pages.views.view_page'),
    url(r'^(?P<slug>[-_\w]+)/$', 'itdagene.app.pages.views.view_page'),
    url(r'^(?P<slug>[-_\w]+)/edit/$', 'itdagene.app.pages.views.edit'),
    url(r'^(?P<lang_code>[a-z][a-z])/(?P<slug>[-_\w]+)/$', 'itdagene.app.pages.views.view_page'),
    url(r'^(?P<lang_code>[a-z][a-z])/(?P<slug>[-_\w]+)/edit/$', 'itdagene.app.pages.views.edit'),
]

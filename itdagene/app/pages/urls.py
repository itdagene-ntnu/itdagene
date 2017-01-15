from django.conf.urls import url
from itdagene.app.pages.views import admin, add, view_page, edit

urlpatterns = [
    url(r'^pages/$', admin, name='pages'),
    url(r'^pages/add/$', add, name='itdagene.app.pages.views.add'),
    url(r'^$', view_page),
    url(r'^(?P<slug>[-_\w]+)/$', view_page),
    url(r'^(?P<slug>[-_\w]+)/edit/$', edit),
    url(r'^(?P<lang_code>[a-z][a-z])/(?P<slug>[-_\w]+)/$', view_page),
    url(r'^(?P<lang_code>[a-z][a-z])/(?P<slug>[-_\w]+)/edit/$', edit),
]

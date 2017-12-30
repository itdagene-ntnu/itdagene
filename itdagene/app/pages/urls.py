from django.urls import re_path

from itdagene.app.pages.views import add, admin, edit, view_page

urlpatterns = [
    re_path(r'^pages/$', admin, name='pages'),
    re_path(r'^pages/add/$', add, name='itdagene.app.pages.views.add'),
    re_path(r'^$', view_page),
    re_path(r'^(?P<slug>[-_\w]+)/$', view_page),
    re_path(r'^(?P<slug>[-_\w]+)/edit/$', edit),
    re_path(r'^(?P<lang_code>[a-z][a-z])/(?P<slug>[-_\w]+)/$', view_page),
    re_path(r'^(?P<lang_code>[a-z][a-z])/(?P<slug>[-_\w]+)/edit/$', edit),
]

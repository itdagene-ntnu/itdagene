# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns

urlpatterns = patterns('itdagene.app.api.views',
    url(r'^users/$', 'users.get'),
    url(r'^worker/(?P<username>\w+)/$', 'workschedule.get'),
    url(r'^workers/$', 'workschedule.list'),
    url(r'^admin/cache/flush/$', 'admin.cache.flush'),
)
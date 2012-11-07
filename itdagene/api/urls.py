# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns

urlpatterns = patterns('itdagene.api.views',
    url(r'^users/$', 'users.get'),
    url(r'^worker/(?P<username>\w+)/$', 'workschedule.get'),

)

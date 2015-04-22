# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import include, patterns, url

urlpatterns = patterns('itdagene.app.comments.views',
    url(r'^add/$', 'add'),
)

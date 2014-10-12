# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('itdagene.app.comments.views',
    url(r'^add/$', 'add'),
)

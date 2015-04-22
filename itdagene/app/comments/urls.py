# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('itdagene.app.comments.views',
                       url(r'^add/$', 'add'), )

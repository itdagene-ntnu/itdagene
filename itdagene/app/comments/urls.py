# -*- coding: utf-8 -*-
from django.conf.urls import url

urlpatterns = [
    url(r'^add/$', 'itdagene.app.comments.views.add'),
]

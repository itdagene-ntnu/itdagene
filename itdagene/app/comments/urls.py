from django.urls import re_path

from itdagene.app.comments.views import add

urlpatterns = [
    re_path(r'^add/$', add, name='itdagene.comments.add'),
]

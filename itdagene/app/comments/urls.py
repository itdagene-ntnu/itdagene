from django.conf.urls import url

from itdagene.app.comments.views import add

urlpatterns = [
    url(r'^add/$', add),
]

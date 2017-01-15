from django.conf.urls import url
from itdagene.app.experiences import views

urlpatterns = [
    url(r'^$', views.list, name='itdagene.app.experiences.views.list'),
    url(r'^add$', views.add, name='itdagene.app.experiences.views.add'),
    url(r'^(?P<id>\d+)/$', views.view, name='itdagene.app.experiences.views.view'),
    url(r'^(?P<id>\d+)/edit$', views.edit, name='itdagene.app.experiences.views.edit'),
]

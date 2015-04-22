from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'itdagene.app.experiences.views.list'),
    url(r'^add$', 'itdagene.app.experiences.views.add'),
    url(r'^(?P<id>\d+)/$', 'itdagene.app.experiences.views.view'),
    url(r'^(?P<id>\d+)/edit$', 'itdagene.app.experiences.views.edit'),
]

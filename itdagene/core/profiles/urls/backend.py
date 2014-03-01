from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(
        regex='^$',
        view='itdagene.core.profiles.views.list',
        name='list'
    ),
    url(
        regex='^(?P<pk>\d+)/$',
        view='itdagene.core.profiles.views.detail',
        name='detail'
    )
)
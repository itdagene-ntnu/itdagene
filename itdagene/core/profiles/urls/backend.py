from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(
        regex='^$',
        view='itdagene.core.profiles.views.profile_list',
        name='list'
    ),
    url(
        regex='^create/$',
        view='itdagene.core.profiles.views.user_create',
        name='user_create'
    ),
    url(
        regex='^(?P<pk>\d+)/$',
        view='itdagene.core.profiles.views.profile_detail',
        name='detail'
    ),
)
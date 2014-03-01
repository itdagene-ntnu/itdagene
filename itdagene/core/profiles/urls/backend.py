from django.conf.urls import patterns, url

urlpatterns = patterns(
    'itdagene.core.profiles.views',
    url(
        regex='^$',
        view='profile_list',
        name='list'
    ),
    url(
        regex='^all/$',
        view='profile_list_all',
        name='list_all'
    ),
    url(
        regex='^create/$',
        view='user_create',
        name='user_create'
    ),
    url(
        regex='^me/$',
        view='profile_detail_me',
        name='me'
    ),
    url(
        regex='^(?P<pk>\d+)/$',
        view='profile_detail',
        name='detail'
    ),
)
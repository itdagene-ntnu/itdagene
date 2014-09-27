from django.conf.urls import patterns, url

urlpatterns = patterns('itdagene.app.users.views',
    url(
        regex=r'^$',
        view='user_list',
        name='list'
    ),
    url(
        regex=r'^create/$',
        view='user_create',
        name='create'
    ),
    url(
        regex=r'^(?P<pk>\d+)/$',
        view='user_detail',
        name='detail'
    ),
    url(
        regex=r'^(?P<pk>\d+)/edit/$',
        view='user_edit',
        name='edit'
    ),
    url(
        regex=r'^(?P<pk>\d+)/edit/password/$',
        view='user_edit_password',
        name='edit_password'
    ),
    url(
        regex=r'^(?P<pk>\d+)/delete/$',
        view='user_delete',
        name='delete'
    ),
)
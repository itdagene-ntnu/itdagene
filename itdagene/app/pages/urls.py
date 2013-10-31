from django.conf.urls import patterns, url

urlpatterns = patterns('itdagene.app.pages.views',
    url(
        regex=r'^$',
        view='view_page'
    ),
    url(
        regex=r'^pages/$',
        view='admin',
        name='pages'
    ),
    url(
        regex=r'^pages/add$',
        view='add'
    ),
    url(
        regex=r'^(?P<lang_code>[a-z][a-z])/(?P<slug>.*)/edit/$',
        view='edit'
    ),
    url(
        regex=r'^(?P<lang_code>[a-z][a-z])/(?P<slug>.*)/$',
        view='view_page'
    ),
    url(
        regex=r'^(?P<slug>.*)/edit/$',
        view='edit'
    ),
    url(
        regex=r'^(?P<slug>.*)/$',
        view='view_page'


    ),
)

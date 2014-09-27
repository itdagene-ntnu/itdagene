from django.conf.urls import patterns, url

urlpatterns = patterns('itdagene.app.mail.views',
    url(regex=r'^add_mailmapping/$', view='add_mailmapping'),
    url(regex=r'^list_mailmapping/$', view='list_mailmapping'),
    url(regex=r'^(?P<pk>\d+)/change_mailmapping/$', view='change_mailmapping'),
    url(regex=r'^(?P<pk>\d+)/delete_mailmapping/$', view='delete_mailmapping'),
    url(regex=r'^(?P<pk>\d+)/$', view='view_mailmapping'),
)
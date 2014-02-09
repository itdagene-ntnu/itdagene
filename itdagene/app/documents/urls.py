from django.conf.urls import url, patterns

urlpatterns = patterns('itdagene.app.documents.views',
    url(r'^$', 'list_documents', name='documents'),
    url(r'^add/$', 'edit_document', name='add_document'),
    url(r'^(?P<id>\d+)/download/$', 'download_document', name='download_document'),
)
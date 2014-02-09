from django.conf.urls import *

urlpatterns = patterns('itdagene.app.venue.views',
    url(r'^$', 'venue', name='venue'),
    url(r'^stands/add/$', 'edit_stand', name='add_stand'),
    (r'^stands$', 'stands'),
)
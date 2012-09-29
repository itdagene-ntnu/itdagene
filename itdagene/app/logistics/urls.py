from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('itdagene.app.logistics.views.interview_room',
    url(r'^room-registrations/$', 'overview', name='room_registrations'),
    url(r'^room-registrations/add/$', 'edit_room_registration', name='add_room_registration'),
)


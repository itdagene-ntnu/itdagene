from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('itdagene.core.profiles.views',
    url(r'^$', 'public_profiles', name='public_profiles'),
    url(r'^all/$', 'profiles', name='profiles'),
    (r'^me/edit$', 'edit_me'),
    url(r'^me/passwd$', 'change_password', name='change_password'),
    (r'^me$', 'me'),
    (r'^(?P<id>\d+)/edit$', 'edit'),
    (r'^(?P<id>\d+)/$', 'profile'),
    (r'^search', 'search'),
)

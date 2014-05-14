from django.conf.urls import patterns, url

urlpatterns = patterns('itdagene.core.profiles.views',
    url(r'^$', 'public_profiles', name='public_profiles'),
)

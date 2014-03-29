from django.conf import settings
from django.conf.urls import url, patterns, include

from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponsePermanentRedirect

admin.autodiscover()

from itdagene.app.twitter.views import TwitterView

#Robots
#urlpatterns = patterns('',
#    url(r'^robots\.txt$', lambda r: HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")),
#)

urlpatterns = patterns('',
    url(r'^experiences/', include('itdagene.app.experiences.urls')),
    url(r'^quiz/', include('itdagene.app.quiz.urls')),
    url(r'^slaves/$', 'itdagene.app.workschedule.views.public_list'),
    url(r'^slaves/(?P<id>\d+)$', 'itdagene.app.workschedule.views.view_public_task'),
    url(r'^api/', include('itdagene.api.urls')),
    url(r'^admin/', include('itdagene.app.admin.urls')),
    url(r'^comments/', include('itdagene.app.comments.urls')),
    url(r'^documents/', include('itdagene.app.documents.urls')),
    url(r'^events/', include('itdagene.app.events.urls')),
    url(r'^feedback/', include('itdagene.app.feedback.urls')),
    url(r'^fp/', include('itdagene.app.frontpage.urls')),
    url(r'^meetings/', include('itdagene.app.meetings.urls')),
    url(r'^news/', include('itdagene.app.news.urls')),
    url(r'^profiles/', include('itdagene.core.profiles.urls')),
    url(r'^dadmin/', include(admin.site.urls)),
    url(r'^$', 'itdagene.app.frontpage.views.frontpage', name='frontpage'),
    url(r'^what-we-offer/$', 'itdagene.app.frontpage.views.what_we_offer', name='what_we_offer'),
    url(r'^(?P<lang_code>[a-z][a-z])/what-we-offer/$', 'itdagene.app.frontpage.views.what_we_offer'),
    url(r'^bdb/', include('itdagene.app.company.urls')),
    url(r'^career/', include('itdagene.app.career.urls')),
    url(r'^todo/', include('itdagene.app.todo.urls')),
    url(r'^venue/', include('itdagene.app.venue.urls')),
    url(r'^workschedules/', include('itdagene.app.workschedule.urls')),
    url(r'^logistics/', include('itdagene.app.logistics.urls')),
    url(r'^forgot-password/$', 'itdagene.core.views.forgot_password', name='forgot_password'),
    url(r'^program/$', 'itdagene.app.events.views.public_event_list', name='program'),
    url(r'^evaluate/(?P<hash>[a-zA-Z0-9]+)/$', 'itdagene.app.feedback.views.evalutions.handle_evaluation', name='evaluate'),
    url(r'^twitter/$', TwitterView.as_view()),
    url(
        regex='^backend/profile/',
        view=include('itdagene.core.profiles.urls.backend', namespace='profile_backend')
    ),
    url(
        regex='^backend/users/',
        view=include('itdagene.app.users.urls', namespace='users')
    ),
)

#urlpatterns += ('itdagene.app.company.views',
#    url(r'^hsp/$', 'hsp')
#)

urlpatterns += patterns('',
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout'),
    url(r'^accounts/profile/$', lambda r: HttpResponsePermanentRedirect('/profiles/me')),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
    url(r'^profile/$', lambda r: HttpResponsePermanentRedirect('/profiles/me')),
    url(r'^accounts/$', lambda r: HttpResponsePermanentRedirect('/profiles/me')),

    #redirects
    url(r'^jobb/$', lambda r: HttpResponsePermanentRedirect(reverse('joblistings'))),
)
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
        (r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': settings.MEDIA_ROOT}),
    )

#Must be the last one
urlpatterns += patterns('', url(r'^', include('itdagene.app.pages.urls')),)


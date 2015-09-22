from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.http import HttpResponsePermanentRedirect

handler403 = 'itdagene.core.views.error403'
handler404 = 'itdagene.core.views.error404'
handler500 = 'itdagene.core.views.error500'

urlpatterns = [
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout',
        {'next_page': 'itdagene.app.frontpage.views.inside'}),
    url(r'^$', 'itdagene.app.frontpage.views.frontpage'),
    url(r'^frontpage/$', 'itdagene.app.frontpage.views.public'),

    url(r'^dashboard/$', 'itdagene.app.frontpage.views.inside'),
    url(r'^dashboard/tweet/$', 'itdagene.app.frontpage.views.tweet'),

    url(r'^users/', include('itdagene.app.users.urls')),
    url(r'^todo/', include('itdagene.app.todo.urls')),
    url(r'^errors/error403/$', 'itdagene.core.views.error403'),
    url(r'^errors/error404/$', 'itdagene.core.views.error404'),
    url(r'^errors/error500/$', 'itdagene.core.views.error500'),
    url(r'^under-development/$', 'itdagene.core.views.under_development'),
    url(r'^experiences/', include('itdagene.app.experiences.urls')),
    url(r'^admin/', include('itdagene.app.itdageneadmin.urls')),
    url(r'^comments/', include('itdagene.app.comments.urls')),
    url(r'^events/', include('itdagene.app.events.urls')),
    url(r'^feedback/', include('itdagene.app.feedback.urls')),
    url(r'^frontpage/', include('itdagene.app.frontpage.urls')),
    url(r'^meetings/', include('itdagene.app.meetings.urls')),
    url(r'^news/', include('itdagene.app.news.urls')),
    url(r'^bdb/', include('itdagene.app.company.urls')),
    url(r'^career/', include('itdagene.app.career.urls')),
    url(r'^workschedules/', include('itdagene.app.workschedule.urls')),
    url(r'^evaluate/(?P<hash>[a-zA-Z0-9]+)/$',
        'itdagene.app.feedback.views.evalutions.handle_evaluation',
        name='evaluate'),

    url(r'^quiz/', include('itdagene.app.quiz.urls', namespace='quiz')),
    url(r'^superadmin/', include(admin.site.urls)),
]

# Redirects
urlpatterns += [
    url(r'^jobb/$', lambda r: HttpResponsePermanentRedirect(
        reverse('itdagene.app.frontpage.views.joblistings'))),
]

# Static files
if settings.DEBUG:
    urlpatterns += \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Must be the last one
urlpatterns += [url(r'^', include('itdagene.app.pages.urls')), ]

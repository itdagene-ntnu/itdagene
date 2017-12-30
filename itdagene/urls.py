from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.urls import reverse
from django.http import HttpResponsePermanentRedirect

from itdagene.app.feedback.views.evalutions import handle_evaluation
from itdagene.app.frontpage.views import frontpage, inside, public, tweet
from itdagene.core.views import error403, error404, error500, under_development

from django.urls import include, re_path

handler403 = error403
handler404 = error404
handler500 = error500

urlpatterns = [
    re_path(r'^login/$', login, name='login'),
    re_path(r'^logout/$', logout,
            {
                'next_page': inside
            }),
    re_path(r'^$', frontpage),
    re_path(r'^frontpage/$', public),
    re_path(r'^dashboard/$', inside),
    re_path(r'^dashboard/tweet/$', tweet),
    re_path(r'^users/', include('itdagene.app.users.urls')),
    re_path(r'^todo/', include('itdagene.app.todo.urls')),
    re_path(r'^errors/error403/$', error403),
    re_path(r'^errors/error404/$', error404),
    re_path(r'^errors/error500/$', error500),
    re_path(r'^under-development/$', under_development),
    re_path(r'^experiences/', include('itdagene.app.experiences.urls')),
    re_path(r'^admin/', include('itdagene.app.itdageneadmin.urls')),
    re_path(r'^comments/', include('itdagene.app.comments.urls')),
    re_path(r'^events/', include('itdagene.app.events.urls')),
    re_path(r'^feedback/', include('itdagene.app.feedback.urls')),
    re_path(r'^frontpage/', include('itdagene.app.frontpage.urls')),
    re_path(r'^meetings/', include('itdagene.app.meetings.urls')),
    re_path(r'^news/', include('itdagene.app.news.urls')),
    re_path(r'^bdb/', include('itdagene.app.company.urls')),
    re_path(r'^career/', include('itdagene.app.career.urls')),
    re_path(r'^workschedules/', include('itdagene.app.workschedule.urls')),
    re_path(r'^evaluate/(?P<hash>[a-zA-Z0-9]+)/$', handle_evaluation, name='evaluate'),
    re_path(r'^quiz/', include('itdagene.app.quiz.urls', namespace='quiz')),
    re_path(r'^superadmin/', admin.site.urls),
]

# Redirects
urlpatterns += [
    re_path(r'^jobb/$', lambda r: HttpResponsePermanentRedirect(
        reverse('itdagene.app.frontpage.views.joblistings'))),
]

# Static files
if settings.DEBUG:
    urlpatterns += \
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Must be the last one
urlpatterns += [
    re_path(r'^', include('itdagene.app.pages.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

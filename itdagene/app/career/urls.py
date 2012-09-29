from django.conf.urls.defaults import url, patterns


urlpatterns = patterns('itdagene.app.career.views.joblistings',
    url(r'^joblistings/$', 'list_joblistings', name='joblistings'),
    url(r'^joblistings/(?P<id>\d+)/edit/$', 'edit', name='edit_joblisting'),
    url(r'^joblistings/(?P<id>\d+)/deactivate/$', 'deactivate', name='deactivate_joblisting'),
    url(r'^joblistings/(?P<id>\d+)/$', 'view_joblisting', name='view_joblisting'),
    url(r'^joblistings/add/(?P<company_id>\d+)/$', 'edit', name='add_joblisting'),
)

urlpatterns += patterns('itdagene.app.career.views.companies',
    url(r'^companies/(?P<id>\d+)/$', 'company_profile', name='company_profile'),
)
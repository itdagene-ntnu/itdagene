from django.conf.urls import patterns, url

urlpatterns = patterns('itdagene.app.company.views',
            url(r'^companies/$', 'list_companies', name='companies'),
            url(r'^companies/(?P<id>\d+)/$', 'view', name='view_company'),
            url(r'^companies/add/$', 'add'),
            url(r'^companies/(?P<id>\d+)/edit$', 'edit'),

            url(r'^companies/(?P<id>\d+)/book/$', 'book_company'),
            url(r'^companies/(?P<id>\d+)/waiting_list', 'waiting_list'),
            url(r'^companies/(?P<id>\d+)/set-status$', 'set_status'),

            url(r'^companies/responsibilities/$', 'set_responsibilities'),
)

urlpatterns += patterns('itdagene.app.company.views.company_contacts',
            url(r'^contacts/(?P<company>\d+)/add/$', 'add_contact'),
            url(r'^contacts/(?P<id>\d+)/vcard$', 'vcard'),
            url(r'^contacts/(?P<contact_id>\d+)/edit/$', 'edit_contact', name='edit_company_contact'),
            url(r'^contacts/(?P<contact_id>\d+)/delete/', 'delete_contact', name='delete_company_contact'),
)
urlpatterns += patterns('itdagene.app.company.views.contracts',
            url(r'^contracts/(?P<company_id>\d+)/add/$', 'add_contract'),
            url(r'^contracts/(?P<company_id>\d+)/edit/(?P<id>\d+)/$', 'edit_contract'),
            url(r'^contracts/(?P<company_id>\d+)/download/(?P<id>\d+)/$', 'download_contract'),
)



urlpatterns += patterns('itdagene.app.company.views.packages',
            url(r'^packages/$', 'list'),
            url(r'^packages/add$', 'add'),
            url(r'^packages/(?P<id>\d+)/$', 'view'),
            url(r'^packages/(?P<id>\d+)/edit$', 'edit'),
)




urlpatterns += patterns('itdagene.app.company.views.economics',
            url(r'^economics/$', 'economic_overview'),
)

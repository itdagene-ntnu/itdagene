from django.conf.urls.defaults import url, patterns

urlpatterns = patterns('itdagene.app.company.views',
            url(r'^companies/$', 'list_companies', name='companies'),
            url(r'^companies/inactive/$', 'inactive'),
            url(r'^companies/hsp/$', 'hsp'),
            url(r'^companies/add/$', 'edit'),
            url(r'^companies/(?P<id>\d+)/$', 'view', name='view_company'),
            url(r'^companies/(?P<id>\d+)/edit$', 'edit'),
            url(r'^companies/(?P<id>\d+)/activate$', 'activate'),
            url(r'^companies/(?P<id>\d+)/deactivate$', 'deactivate'),
            url(r'^companies/(?P<id>\d+)/book/$', 'book_company', name='book_company'),
            url(r'^companies/(?P<id>\d+)/log/$', 'log_company', name='log_company'),
            url(r'^companies/responsibilities/$', 'set_responsibilities'),
            url(r'^companies/contacts-count/$', 'view_contact_count'),
)

urlpatterns += patterns('itdagene.app.company.views.packages',
            url(r'^packages/$', 'list', name='packages'),
            url(r'^packages/add$', 'edit'),
            url(r'^packages/(?P<id>\d+)/$', 'view'),
            url(r'^packages/(?P<id>\d+)/edit$', 'edit'),
)

urlpatterns += patterns('itdagene.app.company.views.comments',
            url(r'^comments/$', 'list_comments'),
            url(r'^comment$', 'comment'),
)

urlpatterns += patterns('itdagene.app.company.views.admin',
    url(r'^admin/$', 'overview'),
)

urlpatterns += patterns('itdagene.app.company.views.company_contacts',
            url(r'^contacts/(?P<company_id>\d+)/add/$', 'edit_contact', name='add_company_contact'),
            url(r'^contacts/(?P<contact_id>\d+)/edit/$', 'edit_contact', name='edit_company_contact'),
            url(r'^contacts/(?P<id>\d+)/vcard$', 'vcard'),
)

urlpatterns += patterns('itdagene.app.company.views.contracts',
            url(r'^contracts/(?P<company_id>\d+)/add/$', 'edit_contract', name='add_contract'),
            url(r'^contracts/(?P<company_id>\d+)/edit/(?P<id>\d+)/$', 'edit_contract', name='edit_contract'),
            url(r'^contracts/(?P<company_id>\d+)/download/(?P<id>\d+)/$', 'download_contract', name='download_contract'),
)
urlpatterns += patterns('itdagene.app.company.views.economics',
            url(r'^economics/$', 'economic_overview', name='economic_overview'),
            url(r'^economics/(?P<company_id>\d+)/billed/$', 'billed'),
            url(r'^economics/(?P<company_id>\d+)/not-billed/$', 'not_billed'),
            url(r'^economics/(?P<company_id>\d+)/paid/$', 'paid'),
            url(r'^economics/(?P<company_id>\d+)/not-paid/$', 'not_paid'),
)

urlpatterns += patterns('itdagene.app.company.views.competition',
            url(r'^competition$', 'view', name='view_competition'),
)

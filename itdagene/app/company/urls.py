from django.conf.urls import url

urlpatterns = [
    url(r'^companies/$', 'itdagene.app.company.views.list_companies', name='companies'),
    url(r'^companies/(?P<id>\d+)/$', 'itdagene.app.company.views.view', name='view_company'),
    url(r'^companies/add/$', 'itdagene.app.company.views.add'),
    url(r'^companies/(?P<id>\d+)/edit$', 'itdagene.app.company.views.edit'),
    url(r'^companies/(?P<id>\d+)/book/$', 'itdagene.app.company.views.book_company'),
    url(r'^companies/(?P<id>\d+)/waiting_list', 'itdagene.app.company.views.waiting_list'),
    url(r'^companies/(?P<id>\d+)/set-status$', 'itdagene.app.company.views.set_status'),
    url(r'^companies/responsibilities/$', 'itdagene.app.company.views.set_responsibilities'),

    url(r'^contacts/(?P<company>\d+)/add/$',
        'itdagene.app.company.views.company_contacts.add_contact'),
    url(r'^contacts/(?P<id>\d+)/vcard$', 'itdagene.app.company.views.company_contacts.vcard'),
    url(r'^contacts/(?P<contact_id>\d+)/edit/$',
        'itdagene.app.company.views.company_contacts.edit_contact', name='edit_company_contact'),
    url(r'^contacts/(?P<contact_id>\d+)/delete/',
        'itdagene.app.company.views.company_contacts.delete_contact',
        name='delete_company_contact'),

    url(r'^contracts/(?P<company_id>\d+)/add/$',
        'itdagene.app.company.views.contracts.add_contract'),
    url(r'^contracts/(?P<company_id>\d+)/edit/(?P<id>\d+)/$',
        'itdagene.app.company.views.contracts.edit_contract'),
    url(r'^contracts/(?P<company_id>\d+)/download/(?P<id>\d+)/$',
        'itdagene.app.company.views.contracts.download_contract'),

    url(r'^packages/$', 'itdagene.app.company.views.packages.list'),
    url(r'^packages/add$', 'itdagene.app.company.views.packages.add'),
    url(r'^packages/(?P<id>\d+)/$', 'itdagene.app.company.views.packages.view'),
    url(r'^packages/(?P<id>\d+)/edit$', 'itdagene.app.company.views.packages.edit'),

    url(r'^economics/$', 'itdagene.app.company.views.economics.economic_overview'),
]

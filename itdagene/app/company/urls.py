from django.conf.urls import url
from itdagene.app.company.views import list_companies, view, add, edit, book_company, waiting_list, \
    set_status, set_responsibilities, company_contacts, contracts, packages, economics

urlpatterns = [
    url(r'^companies/$', list_companies, name='companies'),
    url(r'^companies/(?P<id>\d+)/$', view, name='view_company'),
    url(r'^companies/add/$', add, name='itdagene.app.company.views.add'),
    url(r'^companies/(?P<id>\d+)/edit$', edit),
    url(r'^companies/(?P<id>\d+)/book/$', book_company),
    url(r'^companies/(?P<id>\d+)/waiting_list', waiting_list),
    url(r'^companies/(?P<id>\d+)/set-status$', set_status),
    url(r'^companies/responsibilities/$', set_responsibilities, name='itdagene.app.company.views.set_responsibilities'),

    url(r'^contacts/(?P<company>\d+)/add/$',
        company_contacts.add_contact),
    url(r'^contacts/(?P<id>\d+)/vcard$', company_contacts.vcard),
    url(r'^contacts/(?P<contact_id>\d+)/edit/$',
        company_contacts.edit_contact, name='edit_company_contact'),
    url(r'^contacts/(?P<contact_id>\d+)/delete/',
        company_contacts.delete_contact,
        name='delete_company_contact'),

    url(r'^contracts/(?P<company_id>\d+)/add/$',
        contracts.add_contract),
    url(r'^contracts/(?P<company_id>\d+)/edit/(?P<id>\d+)/$',
        contracts.edit_contract),
    url(r'^contracts/(?P<company_id>\d+)/download/(?P<id>\d+)/$',
        contracts.download_contract),

    url(r'^packages/$', packages.list, name='itdagene.app.company.views.packages.list'),
    url(r'^packages/add$', packages.add, name='itdagene.app.company.views.packages.add'),
    url(r'^packages/(?P<id>\d+)/$', packages.view),
    url(r'^packages/(?P<id>\d+)/edit$', packages.edit),

    url(r'^economics/$', economics.economic_overview, name='itdagene.app.company.views.economics.economic_overview'),
]

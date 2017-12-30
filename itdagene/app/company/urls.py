from django.urls import re_path

from itdagene.app.company.views import (
    add, book_company, company_contacts, contracts, economics, edit, list_companies, packages,
    set_responsibilities, set_status, view, waiting_list
)

urlpatterns = [
    re_path(r'^companies/$', list_companies, name='companies'),
    re_path(r'^companies/(?P<id>\d+)/$', view, name='view_company'),
    re_path(r'^companies/add/$', add, name='itdagene.app.company.views.add'),
    re_path(r'^companies/(?P<id>\d+)/edit$', edit),
    re_path(r'^companies/(?P<id>\d+)/book/$', book_company),
    re_path(r'^companies/(?P<id>\d+)/waiting_list', waiting_list),
    re_path(r'^companies/(?P<id>\d+)/set-status$', set_status),
    re_path(
        r'^companies/responsibilities/$', set_responsibilities,
        name='itdagene.app.company.views.set_responsibilities'
    ),
    re_path(r'^contacts/(?P<company>\d+)/add/$', company_contacts.add_contact),
    re_path(r'^contacts/(?P<id>\d+)/vcard$', company_contacts.vcard),
    re_path(
        r'^contacts/(?P<contact_id>\d+)/edit/$', company_contacts.edit_contact,
        name='edit_company_contact'
    ),
    re_path(
        r'^contacts/(?P<contact_id>\d+)/delete/', company_contacts.delete_contact,
        name='delete_company_contact'
    ),
    re_path(r'^contracts/(?P<company_id>\d+)/add/$', contracts.add_contract),
    re_path(r'^contracts/(?P<company_id>\d+)/edit/(?P<id>\d+)/$', contracts.edit_contract),
    re_path(r'^contracts/(?P<company_id>\d+)/download/(?P<id>\d+)/$', contracts.download_contract),
    re_path(r'^packages/$', packages.list, name='itdagene.app.company.views.packages.list'),
    re_path(r'^packages/add$', packages.add, name='itdagene.app.company.views.packages.add'),
    re_path(r'^packages/(?P<id>\d+)/$', packages.view),
    re_path(r'^packages/(?P<id>\d+)/edit$', packages.edit),
    re_path(
        r'^economics/$', economics.economic_overview,
        name='itdagene.app.company.views.economics.economic_overview'
    ),
]

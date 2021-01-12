from django.urls import re_path
from itdagene.app.company.views import (
    add,
    add_key_information,
    book_company,
    company_contacts,
    contracts,
    delete_key_information,
    economics,
    edit,
    list_companies,
    packages,
    set_responsibilities,
    set_status,
    view,
    waiting_list,
)

urlpatterns = [
    re_path(r"^companies/$", list_companies, name="itdagene.company.list_companies"),
    re_path(r"^companies/(?P<id>\d+)/$", view, name="itdagene.company.view"),
    re_path(r"^companies/add/$", add, name="itdagene.company.add"),
    re_path(r"^companies/(?P<id>\d+)/edit$", edit, name="itdagene.company.edit"),
    re_path(
        r"^companies/(?P<id>\d+)/book/$",
        book_company,
        name="itdagene.company.book_company",
    ),
    re_path(
        r"^companies/(?P<id>\d+)/waiting_list",
        waiting_list,
        name="itdagene.company.waiting_list",
    ),
    re_path(
        r"^companies/(?P<id>\d+)/set-status$",
        set_status,
        name="itdagene.company.set_status",
    ),
    re_path(
        r"^key_information/(?P<company>\d+)/add/$",
        add_key_information,
        name="itdagene.company.key_information.add",
    ),
    re_path(
        r"^key_information/(?P<id>\d+)/delete/$",
        delete_key_information,
        name="itdagene.company.key_information.delete",
    ),
    re_path(
        r"^companies/responsibilities/$",
        set_responsibilities,
        name="itdagene.company.set_responsibilities",
    ),
    re_path(
        r"^contacts/(?P<company>\d+)/add/$",
        company_contacts.add_contact,
        name="itdagene.company.company_contacts.add_contact",
    ),
    re_path(
        r"^contacts/(?P<id>\d+)/vcard$",
        company_contacts.vcard,
        name="itdagene.company.company_contacts.vcard",
    ),
    re_path(
        r"^contacts/(?P<contact_id>\d+)/edit/$",
        company_contacts.edit_contact,
        name="itdagene.company.company_contacts.edit_contact",
    ),
    re_path(
        r"^contacts/(?P<contact_id>\d+)/delete/",
        company_contacts.delete_contact,
        name="itdagene.company.company_contacts.delete_contact",
    ),
    re_path(
        r"^contracts/(?P<company_id>\d+)/add/$",
        contracts.add_contract,
        name="itdagene.company.contracts.add_contract",
    ),
    re_path(
        r"^contracts/(?P<company_id>\d+)/edit/(?P<id>\d+)/$",
        contracts.edit_contract,
        name="itdagene.company.contracts.edit_contract",
    ),
    re_path(
        r"^contracts/(?P<company_id>\d+)/download/(?P<id>\d+)/$",
        contracts.download_contract,
        name="itdagene.company.contracts.download_contract",
    ),
    re_path(r"^packages/$", packages.list, name="itdagene.company.packages.list"),
    re_path(r"^packages/add$", packages.add, name="itdagene.company.packages.add"),
    re_path(
        r"^packages/(?P<id>\d+)/$", packages.view, name="itdagene.company.packages.view"
    ),
    re_path(
        r"^packages/(?P<id>\d+)/edit$",
        packages.edit,
        name="itdagene.company.packages.edit",
    ),
    re_path(
        r"^economics/$",
        economics.economic_overview,
        name="itdagene.company.economics.economic_overview",
    ),
]

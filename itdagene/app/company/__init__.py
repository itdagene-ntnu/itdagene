from django.utils.translation import gettext_lazy as _


COMPANY_STATUS_NOT_CONTACTED = 0
COMPANY_STATUS_CONTACTED = 4
COMPANY_STATUS_NOT_INTERESTED = 1
COMPANY_STATUS_INTERESTED = 2
COMPANY_STATUS_SIGNED = 3

COMPANY_STATUS = (
    (COMPANY_STATUS_NOT_CONTACTED, _("Not contacted")),
    (COMPANY_STATUS_CONTACTED, _("Contacted")),
    (COMPANY_STATUS_NOT_INTERESTED, _("Not interested")),
    (COMPANY_STATUS_INTERESTED, _("Interested")),
    (COMPANY_STATUS_SIGNED, _("Signed")),
)

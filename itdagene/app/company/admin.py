from django.contrib import admin
from itdagene.app.company.models import (
    CallTeam,
    Company,
    CompanyContact,
    Contract,
    Package,
)

admin.site.register(Package)
admin.site.register(CompanyContact)
admin.site.register(Company)
admin.site.register(Contract)
admin.site.register(CallTeam)

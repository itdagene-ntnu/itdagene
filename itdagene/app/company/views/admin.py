from datetime import date
from itdagene.app.company.models import Company, Contract
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render

@permission_required('company.change_company')
def overview(request):
    contracts = Contract.objects.filter(timestamp__year=date.today().year)
    interview_rooms = sum([c.interview_room for c in contracts])
    joblistings = sum([c.joblistings for c in contracts])
    banquet_tickets = sum([c.banquet_tickets for c in contracts])
    return render(request, 'company/admin/overview.html',
            {'interview_rooms': interview_rooms,
             'banquet_tickets': banquet_tickets,
             'joblistings': joblistings})



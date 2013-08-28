from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from itdagene.app.company.models import CallTeam, Company

@permission_required('company.change_company')
def view(request):
    users = User.objects.values('username', 'first_name', 'last_name').filter(is_active = True, profile__type = 'b').exclude(username = "backup-db").annotate(num_contracts = Count('contract_creator')).order_by('-num_contracts')
    userlist = {}
    for user in users:
        userlist[user["username"]] = user["num_contracts"]
    teams = []
    for team in CallTeam.objects.all():
        teamSum = 0
        for person in team.users.all():
            teamSum += userlist[person.username]
        teams.append((teamSum, team))
    teams.sort(reverse=True)

    return render(request, 'company/competition/view.html', {'users': users, 'teams': teams})

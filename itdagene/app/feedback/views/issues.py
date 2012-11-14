from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.template.context import RequestContext
from itdagene.app.feedback.forms import IssueForm, IssueAssignForm
from itdagene.app.feedback.models import Issue
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.shortcuts import render

@permission_required('feedback.change_issue')
def list (request, solved=False):
    bugs = Issue.objects.filter(is_solved=solved, type=0)
    features = Issue.objects.filter(is_solved=solved, type=1)
    cache_bugs = Issue.objects.filter(is_solved=solved, type=2)
    return render(request, 'feedback/issues/list.html',
                             {'bugs': bugs,
                              'features': features,
                              'cache_bugs': cache_bugs})

@permission_required('feedback.change_issue')
def my_issues (request):
    issues = Issue.objects.filter(assigned_user=request.user).order_by('is_solved')
    return render(request, 'feedback/issues/list.html',
                             {'issues': issues})


@permission_required('feedback.change_issue')
def view (request, id):
    issue = get_object_or_404(Issue, pk=id)
    form = IssueAssignForm(instance=issue)
    if request.method == 'POST':
        form = IssueAssignForm(request.POST,instance=issue)
        if form.is_valid():
            issue = form.save()
    return render(request, 'feedback/issues/view.html',
                             {'issue': issue,
                              'form': form,
                              'form_title': _('Assign a user:')})

@permission_required('feedback.change_issue')
def edit (request, id=None):
    if id:
        issue = get_object_or_404(Issue, pk=id)
        form = IssueForm(instance=issue)
    else:
        issue = None
        form = IssueForm()
    if request.method == 'POST':
        if id: form = IssueForm(request.POST,instance=issue)
        else: form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save()
            return render(request, 'feedback/issues/view.html',
                             {'issue': issue,
                              'message': _('Thanks for the feedback')})

    return render(request, 'feedback/form.html',
                             {'issue': issue,
                              'form': form})

@permission_required('feedback.change_issue')
def solved(request, id):
    issue = get_object_or_404(Issue, pk=id)
    issue.solved_date = datetime.now()
    issue.is_solved = True
    issue.status = 3
    issue.save()
    return redirect(reverse('itdagene.app.feedback.views.issues.list'), args=[request])
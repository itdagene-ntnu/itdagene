from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.messages import SUCCESS, add_message
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from itdagene.app.feedback.forms import IssueAssignForm, IssueForm
from itdagene.app.feedback.models import Issue
from itdagene.core.decorators import staff_required


@staff_required()
def list(request, solved=False):
    bugs = Issue.objects.filter(is_solved=solved, type=0)
    features = Issue.objects.filter(is_solved=solved, type=1)
    cache_bugs = Issue.objects.filter(is_solved=solved, type=2)
    return render(
        request, 'feedback/issues/list.html', {
            'bugs': bugs,
            'features': features,
            'cache_bugs': cache_bugs,
            'title': _('Issues')
        }
    )


@staff_required()
def solved_list(request):
    return list(request, solved=True)


@login_required()
def view(request, id):
    if request.user.is_staff:
        issue = get_object_or_404(Issue, pk=id)
    else:
        issue = get_object_or_404(Issue, pk=id, creator=request.user)

    form = IssueAssignForm(instance=issue)
    if request.method == 'POST':
        form = IssueAssignForm(request.POST, instance=issue)
        if form.is_valid():
            issue = form.save()
    return render(
        request, 'feedback/issues/view.html', {
            'issue': issue,
            'form': form,
            'form_title': _('Assign a user:'),
            'title': _('Issue'),
            'description': issue,
            'now_time': timezone.now()
        }
    )


@permission_required('feedback.add_issue')
def add(request):
    form = IssueForm()
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            form.save()
            add_message(request, SUCCESS, _('Thank you for the feedback.'))
            if request.user.is_staff:
                return redirect(reverse('itdagene.app.feedback.views.issues.list'))
            else:
                return redirect(reverse('itdagene.app.frontpage.views.inside'))

    return render(request, 'feedback/form.html', {'title': _('Add Issue'), 'form': form})


@permission_required('feedback.change_issue')
def edit(request, id=None):
    issue = get_object_or_404(Issue, pk=id)
    form = IssueForm(instance=issue)
    if request.method == 'POST':
        form = IssueForm(request.POST, instance=issue)
        if form.is_valid():
            issue = form.save()
            add_message(request, SUCCESS, _('The issue has changed.'))
            if request.user.is_staff:
                return redirect(reverse('itdagene.app.feedback.views.issues.list'))
            else:
                return redirect(reverse('itdagene.app.frontpage.views.inside'))

    return render(
        request, 'feedback/form.html',
        {
            'title': _('Edit Issue'),
            'description': issue,
            'issue': issue,
            'form': form
        }
    )


@permission_required('feedback.add_issue')
def my_issues(request):
    assigned = Issue.objects.filter(assigned_user=request.user).order_by('is_solved')
    created = Issue.objects.filter(creator=request.user).order_by('is_solved')
    return render(
        request, 'feedback/issues/mine.html', {
            'assigned': assigned,
            'created': created,
            'title': _('My Issues')
        }
    )


@permission_required('feedback.change_issue')
def solved(request, id):
    issue = get_object_or_404(Issue, pk=id)
    issue.solved_date = timezone.now()
    issue.is_solved = True
    issue.status = 3
    issue.save()
    return redirect(reverse('itdagene.app.feedback.views.issues.list'))

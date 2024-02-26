from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.db.models import Prefetch
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils import timezone

from itdagene.app.comments.models import Comment
from itdagene.app.company.models import Company
from itdagene.app.feedback.models import Issue
from itdagene.app.meetings.models import Meeting
from itdagene.app.todo import todo_list


@login_required
def frontpage(request: HttpRequest) -> HttpResponse:
    todos = todo_list(request.user)
    now = timezone.now()

    # Unused variables
    if request.user.is_staff:
        open_issues = Issue.objects.filter(is_solved=False).count()
        assigned_you_issues = Issue.objects.filter(
            is_solved=False, assigned_user=request.user
        ).count()
        overdue_issues = Issue.objects.filter(
            is_solved=False, deadline__lte=timezone.now()
        ).count()
        upcomming_meetings = Meeting.objects.filter(
            replies__user=request.user, replies__is_attending=True, date__gte=now
        ).order_by("date")

        company_type = ContentType.objects.get_for_model(Company)
        company_comments = (
            Comment.objects.filter(content_type=company_type)
            .order_by("-date")[:8]
            .select_related("user", "content_type")
            .prefetch_related(Prefetch("object"))
        )

    return render(request, "frontpage.html", locals())

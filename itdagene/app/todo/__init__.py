def todo_list(user):
    from django.db.models import Q
    from django.utils import timezone

    from itdagene.app.todo.models import Todo

    if user.is_staff:
        return (
            Todo.objects.filter(user=user)
            .filter(Q(finished=True, deadline__gte=timezone.now()) | Q(finished=False))
            .order_by("deadline")
        )
    return None

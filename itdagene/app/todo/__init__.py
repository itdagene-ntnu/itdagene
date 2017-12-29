def todo_list(user):
    from itdagene.app.todo.models import Todo
    from django.db.models import Q
    from datetime import datetime

    if user.is_staff:
        return Todo.objects.filter(
            user=user
        ).filter(Q(finished=True, deadline__gte=datetime.now())
                 | Q(finished=False)).order_by('deadline')
    return None

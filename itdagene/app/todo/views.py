from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from itdagene.app.company.models import Company
from itdagene.app.todo.forms import AddTodoForm, AddCollectiveTodoForm
from itdagene.app.todo.models import Todo
from django.contrib.auth.decorators import permission_required
from itdagene.core.notifications.models import Notification
from django.shortcuts import render


@permission_required('todo.change_todo')
def add_collective_todo(request):
    form = AddCollectiveTodoForm()
    if request.method == 'POST':
        for company in Company.objects.filter(active=True).exclude(contact=None):
            t = Todo(company=company)
            form = AddCollectiveTodoForm(request.POST, instance=t)
            if form.is_valid():
                todo = form.save(commit=False)
                todo.user = todo.company.contact
                todo.save()
                if todo.user:
                    n = Notification(
                        user=todo.user,
                        priority=2,
                        date=datetime.now(),
                        object_id=todo.pk,
                        content_type=ContentType.objects.get_for_model(todo),
                        message='New todo: ' % todo,
                        send_mail=True
                    )
                    n.save()

    return render(request, 'todo/add_collective.html', {'form': form})

@login_required
def add_todo (request):
    if request.method == 'POST':
        form = AddTodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()

            todos = Todo.objects.filter(user=request.user, company=todo.company, finished=False)
            output = ""
            for t in todos:
                output += "<li data-id=\"" + str(t.id) + "\">" + str(t.title) + "</li>"
            return HttpResponse(output)
        return HttpResponse("Something went wrong", status=400)
    else:
        return HttpResponse('No post-data', status=400)

@csrf_exempt
@login_required
def done_todo (request):
    if request.method == 'POST':
        id = request.POST.get('id')
        company = None
        try:
            todo = Todo.objects.get(pk=id, user=request.user)
            todo.finished = True
            todo.save()
            company = todo.company
        except (TypeError, Todo.DoesNotExist):
            return HttpResponse(status=404)

        todos = Todo.objects.filter(user=request.user,company=company, finished=False)
        output = ""
        for t in todos:
            output += "<li data-id=\"" + str(t.id) + "\">" + str(t.title) + "</li>"
        return HttpResponse(output)
    else:
        return HttpResponse('No post-data', status=400)
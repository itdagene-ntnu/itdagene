from django.template.base import Library
from itdagene.app.todo.forms import AddTodoForm
from itdagene.app.todo.models import Todo
from itdagene.core.auth import get_current_user

register = Library()

@register.inclusion_tag('todo/templatetags/list.html', takes_context=True)
def todos_company (context, company):
    todos = Todo.objects.filter(company=company, user=context['user'], finished=False)
    return {'todos': todos}

@register.inclusion_tag('todo/templatetags/form_company.html')
def todo_form_company (company):
    todo = Todo(company=company)
    form = AddTodoForm(instance=todo)
    return {'form': form}
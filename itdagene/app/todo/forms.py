from django.forms.models import ModelForm
from itdagene.app.todo.models import Todo

class AddTodoForm (ModelForm):
    class Meta:
        model = Todo
        fields = ('title','company')

class AddCollectiveTodoForm (ModelForm):
    class Meta:
        model = Todo
        exclude = ('company', 'milestone', 'user', 'finished')
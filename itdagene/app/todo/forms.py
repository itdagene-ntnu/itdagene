from django.forms.models import ModelForm
from itdagene.app.todo.models import Todo
from itdagene.core.models import User
from itdagene.core.auth import get_current_user


class TodoForm (ModelForm):

    def __init__(self, *args, **kwargs):
        super(TodoForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(is_staff=True)
        self.fields['user'].initial = get_current_user()

    class Meta:
        model = Todo
        fields = ('description', 'user', 'deadline')

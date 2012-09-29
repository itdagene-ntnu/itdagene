from itdagene.app.logistics.models import RoomRegistration
from django.forms.models import ModelForm
from itdagene.core.models import BaseModel

class RoomRegistrationForm(ModelForm):
    class Meta:
        model = RoomRegistration
        exclude = BaseModel.exclude_fields()

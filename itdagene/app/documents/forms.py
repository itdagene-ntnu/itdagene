from itdagene.app.documents.models import Document
from django.forms.models import ModelForm

class DocumentForm (ModelForm):
    class Meta:
        model = Document

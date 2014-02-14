from django.core.urlresolvers import reverse
from django.http import HttpResponse
from itdagene.app.documents.forms import DocumentForm
from itdagene.app.documents.models import Document
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect, get_object_or_404


@permission_required('documents.change_document')
def list_documents(request):
    documents = []
    years = []
    documents = Document.objects.all()
    return render(request, 'documents/base.html', {'documents': documents})


@permission_required('documents.change_document')
def edit_document(request, id=None):
    form = DocumentForm()
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save()
            request.session['message'] = {'class': 'success', 'value': _('%s was uploaded') % document.file.name}
            return redirect(reverse('documents'))
    return render(request, 'documents/form.html', {'form': form})


@permission_required('documents.change_document')
def download_document(request, id):
    import os
    doc = get_object_or_404(Document,pk=id)
    abspath = open(doc.file.path,'r')
    response = HttpResponse(content=abspath.read())
    response['Content-Type']= 'application/octet-stream'
    response['Content-Disposition'] = 'attachment; filename=%s'\
    % os.path.basename(doc.file.path)
    return response
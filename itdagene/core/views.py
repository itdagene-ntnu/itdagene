from django.conf import settings
from django.http import HttpResponse, Http404
from django.utils.translation import ugettext_lazy as _
from django.template.context import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from itdagene.core.auth import generate_password
from itdagene.core.profiles.forms import ForgotPasswordForm
from django.shortcuts import render
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core import management

def permission_denied (request, args=None):
    """
    View that displays permission denied and info about the permission that is required
    """
    return render(request,'core/permission_denied.html', args)

def forgot_password (request):
    form = ForgotPasswordForm()
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                password = generate_password()
                user.set_password(password)
                user.save()
                send_mail(_('Your password for itDAGENE'),_('Your new password is: ' + password),settings.FROM_ADDRESS,(user.email,))
                return redirect(reverse('itdagene.core.profiles.views.me'))
            except(TypeError, User.DoesNotExist):
                pass

    return render(request,'forgot_password.html',{'form':form})

@csrf_exempt
def backup_for_remote (request):
    import os
    if request.method == 'POST':
        u = get_object_or_404(User, username=request.POST.get('username'))
        if u.check_password(request.POST.get('password')):
            path = management.call_command('backup')
            if path: return HttpResponse('Could not make a backup')
            else:
                abspath = open(path,'r')
                response = HttpResponse(content=abspath.read())
                response['Content-Type']= 'application/octet-stream'
                response['Content-Disposition'] = 'attachment; filename=%s'\
                % os.path.basename(path)
            return response
    raise Http404
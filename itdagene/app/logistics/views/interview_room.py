from django.core.urlresolvers import reverse
from itdagene.app.logistics.forms import RoomRegistrationForm
from itdagene.app.logistics.models import RoomRegistration
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect

@permission_required('logistics.change_roomregistration')
def overview(request):
    room_registrations = RoomRegistration.objects.all()
    return render(request, 'logistics/interview_rooms/base.html', {'room_registrations': room_registrations})

@permission_required('logistics.change_roomregistration')
def edit_room_registration (request, id=None):
    if id:
        room_registration = get_object_or_404(RoomRegistration, pk=id)
    else:
        room_registration = None
    form = RoomRegistrationForm(instance=room_registration)
    if request.method == 'POST':
        form = RoomRegistrationForm(request.POST, instance=room_registration)
        if form.is_valid():
            form.save()
            return redirect(reverse('room_registrations'))

    return render(request, 'logistics/interview_rooms/form.html', {'form': form})

# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from itdagene.api.util import login_or_token_required, render_json
from itdagene.core.models import UserProxy as User

@login_or_token_required()
def get(request, id=None):
    if id is not None:
        try:
            user_data = User.objects.get(pk=id)

            return render_json({'workout': user_data.as_dict()})

        except (TypeError, User.DoesNotExist):
            return render_json(error=_('Could not find user'))

    else:
        data = []
        for user_data in User.objects.filter(is_active=True):
            data.append(user_data.as_dict())
        return render_json({'users': data})
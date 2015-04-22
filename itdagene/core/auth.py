import string
from new import instancemethod
from random import choice

from django.conf import settings
from django.contrib.auth.models import AnonymousUser

USER_ATTR_NAME = getattr(settings, 'LOCAL_USER_ATTR_NAME', '_current_user')

try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local
_thread_locals = local()


def _do_set_current_user(user_fun):
    setattr(_thread_locals, USER_ATTR_NAME,
            instancemethod(user_fun, _thread_locals, type(_thread_locals)))


def _set_current_user(user=None):

    _do_set_current_user(lambda self: user)


class LocalUserMiddleware(object):
    def process_request(self, request):
        # request.user closure; asserts laziness; memoization is implemented in
        # request.user (non-data descriptor)
        _do_set_current_user(lambda self: getattr(request, 'user', None))
        if get_current_user().is_authenticated():
            request.session['django_language'] = get_current_user().language
        else:
            request.session['django_language'] = 'nb'


def get_current_user():
    from models import User
    try:
        current_user = getattr(_thread_locals, USER_ATTR_NAME, None)
        return current_user() if current_user else current_user
    except (TypeError, User.DoesNotExist):
        return AnonymousUser


def generate_password(length=8, chars=string.letters + string.digits):
    return ''.join([choice(chars) for i in range(length)])

import string
from new import instancemethod
from random import choice
from threading import local

from django.conf import settings
from django.contrib.auth.models import AnonymousUser

USER_ATTR_NAME = getattr(settings, 'LOCAL_USER_ATTR_NAME', '_current_user')


_thread_locals = local()


def _do_set_current_user(user_function):
    setattr(_thread_locals, USER_ATTR_NAME,
            instancemethod(user_function, _thread_locals, type(_thread_locals)))


def _set_current_user(user=None):
    _do_set_current_user(lambda self: user)


def get_current_user():
    from models import User
    try:
        current_user = getattr(_thread_locals, USER_ATTR_NAME, None)
        return current_user() if current_user else current_user
    except (TypeError, User.DoesNotExist):
        return AnonymousUser


def generate_password(length=8, chars=string.letters + string.digits):
    return ''.join([choice(chars) for i in range(length)])

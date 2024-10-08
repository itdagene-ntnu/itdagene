from collections.abc import Callable
from random import choices
from string import ascii_letters, digits
from threading import local
from typing import Any

from django.conf import settings
from django.contrib.auth.models import AnonymousUser


USER_ATTR_NAME = getattr(settings, "LOCAL_USER_ATTR_NAME", "_current_user")

_thread_locals = local()


def set_current_user_function(user_function: Callable) -> None:
    setattr(_thread_locals, USER_ATTR_NAME, user_function)


def set_current_user(user: Any = None) -> None:
    set_current_user_function(lambda _: user)


def get_current_user():
    # Problems when top-layer import from core/models.py
    from itdagene.core.models import User

    current_user = getattr(_thread_locals, USER_ATTR_NAME, None)

    try:
        return current_user() if current_user else current_user
    except (TypeError, User.DoesNotExist):
        return AnonymousUser


def generate_password(length: int = 8, chars: str = ascii_letters + digits) -> str:
    return "".join(choices(chars, k=length))

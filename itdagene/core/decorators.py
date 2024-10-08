from collections.abc import Callable
from typing import Any, Optional

from django.contrib.auth.decorators import user_passes_test


def superuser_required(
    login_url: Optional[str] = None, raise_exception: Any = False
) -> Callable:
    def check_perms(user) -> bool:
        return user.is_superuser

    return user_passes_test(check_perms, login_url)


def staff_required(
    login_url: Optional[str] = None, raise_exception: Any = False
) -> Callable:
    def check_perms(user) -> bool:
        return user.is_staff

    return user_passes_test(check_perms, login_url)

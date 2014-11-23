from django.contrib.auth.decorators import user_passes_test

try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps


def superuser_required(login_url=None, raise_exception=False):
    def check_perms(user):
        return user.is_superuser
    return user_passes_test(check_perms, login_url=login_url)

def staff_required(login_url=None, raise_exception=False):
    def check_perms(user):
        return user.is_staff
    return user_passes_test(check_perms, login_url=login_url)

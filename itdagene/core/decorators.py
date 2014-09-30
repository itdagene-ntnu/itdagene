from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.4 fallback.

from django.http import Http404

def staff_or_404(view_func):
    """
    Decorator for views that checks that the user is logged in and is a staff
    member, raising a 404 if necessary.
    """
    def _checklogin(request, *args, **kwargs):
        if request.user.is_active and request.user.is_staff:
            # The user is valid. Continue to the admin page.
            return view_func(request, *args, **kwargs)

        else:
            raise Http404

    return wraps(view_func)(_checklogin)

def dev_or_login_required(view_func):
    def _checklogin(request, *args, **kwargs):
        if request.user.is_authenticated():
            return view_func(request, *args, **kwargs)

        else:
            if settings.DEBUG:
                return view_func(request, *args, **kwargs)
            else:
                return redirect("/accounts/login/?next=%s" % (request.path))

    return wraps(view_func)(_checklogin)



def superuser_required(login_url=None, raise_exception=False):
    def check_perms(user):
        return user.is_superuser
    return user_passes_test(check_perms, login_url=login_url)

def staff_required(login_url=None, raise_exception=False):
    def check_perms(user):
        return user.is_staff
    return user_passes_test(check_perms, login_url=login_url)
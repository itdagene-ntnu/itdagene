from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import HttpRequest
from django.utils.cache import get_cache_key
from django.core.cache.backends.dummy import DummyCache
from django.core.cache.backends.memcached import BaseMemcachedCache


def expire_page_cache(view, args=None):
    """
    Removes cache created by cache_page functionality.
    Parameters are used as they are in reverse()
    """
    try:
        if args is None:
            path = reverse(view)
        else:
            path = reverse(view, args=args)

        request = HttpRequest()
        request.path = path
        key = get_cache_key(request)
        if cache.has_key(key):
            cache.delete(key)
    except:
        pass


def flush_cache():
    """
    Flushes entire cache
    """
    if type(cache) is DummyCache:
        return
    cache._cache.flush_all()
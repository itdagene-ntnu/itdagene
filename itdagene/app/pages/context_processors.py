# -*- coding: utf8 -*-
from .models import Page


def menu_pages(request):
    pages = Page.objects.filter(active=True, need_auth=False, menu=True)
    return {
        'menu_pages': pages,
    }

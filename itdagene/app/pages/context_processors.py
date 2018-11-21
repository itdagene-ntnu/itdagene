# -*- coding: utf8 -*-
from .models import Page


def menu_pages(request):

    pages = Page.objects.filter(
        active=True, need_auth=False, menu=True, language=request.LANGUAGE_CODE
    )
    return {
        'menu_pages': pages,
    }

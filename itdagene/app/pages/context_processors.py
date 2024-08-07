from typing import Any

from itdagene.app.pages.models import Page


def menu_pages(request: Any) -> dict:
    pages = Page.objects.filter(active=True, need_auth=False, menu=True)
    return {"menu_pages": pages}

from typing import Any

from django.conf import settings

from itdagene.core.models import Preference


def site_processor(request: Any) -> dict:
    """Find site information in templates."""
    return {"site": settings.SITE}


def utils_processor(request: Any) -> dict:
    """Find site information in templates."""
    return {"preferences": Preference.current_preference()}

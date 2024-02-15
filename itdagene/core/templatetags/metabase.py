from django.conf import settings
from django.template import Library
from jwt import encode

register = Library()


@register.simple_tag
def metabase(dash_id, style) -> str:
    payload = {"resource": {"dashboard": int(dash_id)}, "params": {}}
    token = encode(payload, settings.METABASE_SECRET_KEY, algorithm="HS256")
    return settings.METABASE_SITE_URL + "/embed/dashboard/" + token + style

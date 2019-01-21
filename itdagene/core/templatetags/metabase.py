import jwt
from django.conf import settings
from django.template import Library

register = Library()


@register.simple_tag
def metabase(dash_id, style):
    payload = {"resource": {"dashboard": int(dash_id)}, "params": {}}

    token = jwt.encode(payload, settings.METABASE_SECRET_KEY, algorithm="HS256")

    return (
        settings.METABASE_SITE_URL + "/embed/dashboard/" + token.decode("utf-8") + style
    )

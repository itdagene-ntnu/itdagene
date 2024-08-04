import bleach
from bleach_allowlist import markdown_attrs, markdown_tags
from django.template import Library
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from markdown import markdown


register = Library()


@register.filter(is_safe=True)
@stringfilter
def markdownize(value: str) -> str:
    text = bleach.clean(
        markdown(value, extensions=["nl2br"]), markdown_tags, markdown_attrs
    )
    return mark_safe(text)

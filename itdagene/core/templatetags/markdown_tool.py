from django.template import Library
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from markdown import markdown

register = Library()


@register.filter(is_safe=True)
@stringfilter
def markdownize(value: str) -> str:
    # ! safe_mode and enable_attributes are deprecated
    return mark_safe(
        markdown(
            value,
            extensions=["nl2br"],
            safe_mode=True,
            enable_attributes=False,
        )
    )

import markdown
from django.template import Library
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = Library()


@register.filter(is_safe=True)
@stringfilter
def markdownize(value):
    return mark_safe(
        markdown.markdown(value,
                          extensions=["nl2br"],
                          safe_mode=True,
                          enable_attributes=False))

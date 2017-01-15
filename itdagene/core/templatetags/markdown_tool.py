import markdown
from django.template import Library
from django.template.defaultfilters import stringfilter
#from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

register = Library()


@register.filter(is_safe=True)
@stringfilter
def markdownize(value):
    extensions = ["nl2br", ]

    return mark_safe(markdown.markdown(value, extensions,
                                       safe_mode=True,
                                       enable_attributes=False))

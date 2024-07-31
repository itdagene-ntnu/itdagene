import re

from django.conf import settings
from django.template import Library
from sorl.thumbnail.shortcuts import get_thumbnail


register = Library()


@register.filter
def load_thumbnails(value):
    images = re.findall(
        r'<img class="thumbnail"( alt="([a-zA-Z0-9\.\:\/_ -]+)?")? '
        r'src="([a-zA-Z0-9\.\:\/_ -]+)"([a-zA-Z0-9\.\:\;\/_=" -]+)?>',
        value,
    )
    if settings.DEBUG:
        if settings.TOOLBAR:
            url = "http://127.0.0.1:8000"
        else:
            url = "http://dev.itdagene.no"
    else:
        url = "http://%s" % settings.SITE_URL
    for i in images:
        width = re.search(r"width:( )?(\d+)px;", i[3])
        if width is not None:
            width = int(width.group().replace("width:", "").replace("px;", "").strip())
            if width > 1000:
                width = 1000

            value = value.replace(i[3], f' style="width: {width};"')
        else:
            width = 1000

        float_ = re.search(r"float:([ ]+)?(\w+);", i[3])
        if float_:
            value = value.replace(
                "style=",
                'class="pull-'
                f'{float_.group().replace("float:", "").replace(";", "").strip()}"'
                " style=",
            )

        image = i[2]
        im = get_thumbnail(f"{url}{image}", str(width))
        value = value.replace(image, im.url)
    return value

# -*- coding: utf-8 -*-
import re
from django.conf import settings
from django.template.base import Library
from sorl.thumbnail.shortcuts import get_thumbnail

register = Library()


@register.filter
def load_thumbnails(value):
    images = re.findall('<img class="thumbnail"( alt="([a-zA-Z0-9\.\:\/_ -]+)?")? src="([a-zA-Z0-9\.\:\/_ -]+)"([a-zA-Z0-9\.\:\;\/_=\" -]+)?>', value)
    if settings.DEBUG:
        if settings.TOOLBAR:
            url = "http://127.0.0.1:8000"
        else:
            url = "http://dev.itdagene.no"
    else:
        url = "http://%s" % settings.SITE_URL
    for i in images:
        width = re.search(r'width:( )?(\d+)px;', i[3])
        if width:
            width = int(width.group().replace('width:', '').replace('px;', '').strip())
            if width > 1000:
                width = 1000

            value = value.replace(i[3], ' style="width: %d;"' % width)
        else:
            width = 1000

        float = re.search(r'float:([ ]+)?(\w+);', i[3])
        if float:
            value = value.replace('style=', 'class="pull-%s" style=' % float.group().replace('float:','').replace(';', '').strip())

        image = i[2]
        im = get_thumbnail("%s%s" % (url,image), '%d' % width)
        value = value.replace(image, im.url)
    return value
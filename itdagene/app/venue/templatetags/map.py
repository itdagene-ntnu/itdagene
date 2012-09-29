from django.template.base import Library

register = Library()

@register.simple_tag()
def load_openlayers():
    return '<script src="http://www.openlayers.org/api/OpenLayers.js"></script>'


@register.inclusion_tag('venue/stands/tag_map.html')
def stand_map (stand):
    return {'stand': stand}

@register.inclusion_tag('venue/map.html')
def general_map (stands):
    return {'stands': stands}
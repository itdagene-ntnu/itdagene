from typing import Optional
from django.conf import settings
from sorl.thumbnail import get_thumbnail


def resolve_image_url(image) -> str:
    return f"{settings.HOST_URL}{image.url}"


def resize_image(input_image, **kwargs) -> Optional[str]:
    if not input_image:
        return None

    height = kwargs.get("height")
    width = kwargs.get("width")
    if not height and not width:
        return resolve_image_url(input_image)

    geometry = f"{width}x{height}"

    if width and not height:
        geometry = f"{width}"
    if height and not width:
        geometry = f"x{height}"

    thumb_settings = {
        "format": kwargs.get("format", "PNG"),
        "padding": kwargs.get("padding", True),
        "quality": kwargs.get("quality", 99),
        "padding_color": (255, 255, 255, 0),
        "transparancy": True,
    }

    output_image = get_thumbnail(input_image, geometry, **thumb_settings)

    return resolve_image_url(output_image)

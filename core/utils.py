import os
from django.conf import settings
from django.utils.html import format_html
from django.utils.safestring import mark_safe


def create_thumb(obj):
    # url = obj[field_name].url
    # width = obj[field_name].width
    # hegiht = obj[field_name].height

    return ''

    # thumb_path = f'{settings.BASE_DIR}{url}'

    # if (os.path.exists(thumb_path)):
    #     render_thumb = f'<span style="width: 170px; height: 170px; display: block;"><img style="max-width: 100%; max-height: 100%;" src="{url}" width="{width}" height={height} /></span>'

    #     return mark_safe(render_thumb)
    # else:
    #     return "Can't find image"
    # return format_html(f'<img src="{url}" width="200px" height="auto" />')

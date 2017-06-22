from django.template import Library
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from easy_thumbnails.files import get_thumbnailer


register = Library()


@register.simple_tag
def speaker_url_with_fallback(speaker, crop_size):
    if bool(speaker.photo):
        return get_thumbnailer(speaker.photo).get_thumbnail(
            {'size': (crop_size, crop_size), 'crop': True}
        ).url
    else:
        return static(settings.DEFAULT_FALLBACK_IMAGE)

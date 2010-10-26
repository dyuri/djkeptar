from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


# root of the gallery where the images are store on the filesystem
KEPTAR_ROOT = getattr(settings, 'KEPTAR_ROOT', None)
if KEPTAR_ROOT is None:
    raise ImproperlyConfigured('Please make sure you specified a KEPTAR_ROOT setting.')

# absolute or relative url to reach the images via http (to support static webservers)
KEPTAR_URL = getattr(settings, 'KEPTAR_URL', None)
if KEPTAR_URL is None:
    raise ImproperlyConfigured('Please make sure you specified a KEPTAR_ROOT setting.')

# supported file extensions
KEPTAR_EXTENSIONS = getattr(settings, 'KEPTAR_EXTENSIONS', ['jpg','jpeg','png'])

# thumbnail sizes and folders
KEPTAR_THUMBS = getattr(settings, 'KEPTAR_THUMBS', {
        '': { 'dir': '.tn', 'size': (120,120) },
        'blog': { 'dir': '.tn/blog', 'size': (600,600) },
        })

# show hidden files (files starting with '.')
KEPTAR_SHOW_HIDDEN = getattr(settings, 'KEPTAR_SHOW_HIDDEN', False)

# icon locations (url)
KEPTAR_ICONS = getattr(settings, 'KEPTAR_ICONS', {
        'dir': '/media/keptar/icons/tn_dir.jpg',
        })


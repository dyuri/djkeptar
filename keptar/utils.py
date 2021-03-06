from django.core.urlresolvers import reverse
from keptar import settings
import os, os.path
import Image
try:
    from collections import OrderedDict
except ImportError:
    from keptar.odict import OrderedDict

class AccessDenied(Exception):
    pass

class FileNotFound(Exception):
    pass

class NotDirectory(Exception):
    pass

def enrich(filelist, relpath='', thumbnails=True):
    """A kep neveihez hozzateszi a szukseges adatokat"""

    files = OrderedDict()

    for f in filelist:
        abspath = os.path.abspath(os.path.join(settings.KEPTAR_ROOT, relpath, f))
        if os.path.isdir(abspath):
            thumb = settings.KEPTAR_ICONS.get('dir', None)
            url = reverse('keptar.views.listdir', args=[os.path.join(relpath, f)])
            direct_url = None
            type = 'dir'
        else:
            if thumbnails:
                try:
                    thumb = get_thumbnail(abspath)
                except:
                    thumb = None
            else:
                thumb = settings.KEPTAR_ICONS.get('file', None)
            url = reverse('keptar.views.showfile', args=[os.path.join(relpath, f)])
            direct_url = getattr(settings, 'KEPTAR_URL', '/media/')+relpath+f
            type = 'file'

        # TODO: egyeb adatok
        files[f] = {
                'relpath': relpath,
                'url': url,
                'abspath': abspath,
                'thumb': thumb,
                'type': type,
                'direct_url': direct_url,
                }

    return files


def get_parent(path):
    """A megadott elem szulokonyvtarat adja meg"""

    # security check
    parent = os.path.dirname(path)

    try:
        get_abspath(parent)
    except:
        parent = ''

    return parent


def get_abspath(path):
    """AccessDenied exceptiont dob, ha valaki cselezni akar"""

    abspath = os.path.abspath(os.path.join(settings.KEPTAR_ROOT, path))
    # vajon a celkonyvtar valoban a root-on belul talalhato? - /../... miatt
    if not abspath.startswith(settings.KEPTAR_ROOT):
        raise AccessDenied("%s < %s" % (abspath, settings.KEPTAR_ROOT))
    
    return abspath


def get_filelist(path, show_hidden=getattr(settings, 'KEPTAR_SHOW_HIDDEN', False), thumbnails=True):
    """Visszaadja a ``path`` konyvtarban levo konyvtarak es fileok listajat.
    A ``path`` a ``settings.KEPTAR_ROOT``-hoz relativ.
    A konyvtarak es a fileok listajat ket kulon dict-ben adja vissza, 
    mindenfele extra parameterrel.
    A ``settings.KEPTAR_EXTENSIONS``-nel allithatoak a tamogatott 
    kiterjesztesek.
    """

    abspath = get_abspath(path)

    if not os.path.isdir(abspath):
        raise NotDirectory(abspath)

    dirs = []
    pictures = []

    for fname in os.listdir(abspath):
        file = os.path.join(abspath, fname)
        if os.path.isdir(file) and (show_hidden or not fname.startswith('.')):
            dirs.append(fname)
        if os.path.isfile(file):
            # a kiterjesztes tamogatott-e
            ext = file[file.rfind('.')+1:]
            if ext.lower() in settings.KEPTAR_EXTENSIONS and (show_hidden or not fname.startswith('.')):
                pictures.append(fname)

    dirs.sort()
    pictures.sort()

    return enrich(dirs+pictures, relpath=path)


def get_thumbnail(file, type='', regenerate=False):
    """Visszaadja, illetve ha nem letezik, akkor legeneralja a ``file``-hoz
    tartozo thumbnailt.
    A ``type``-on keresztul mondhatjuk meg, hogy milyen tipusu thumbnailre
    van szuksegunk, a tipusok parametereit a ``settings.py``-ben allithatjuk.
    Ha a ``regenerate`` ``True``, akkor ujrageneralja a thumbnailt.
    """

    ext = file[file.rfind('.')+1:]
    if not os.path.isfile(file) or ext.lower() not in settings.KEPTAR_EXTENSIONS:
        raise FileNotFound(file)
    
    basename = os.path.basename(file)
    dirname = os.path.dirname(file)
    thumbname = os.path.join(dirname, settings.KEPTAR_THUMBS[type]['dir'], basename)
    if regenerate or not os.path.isfile(thumbname):
        if not os.path.isdir(os.path.dirname(thumbname)):
            os.mkdir(os.path.dirname(thumbname))
        generate_thumbnail(file, thumbname, settings.KEPTAR_THUMBS[type]['size'])
    
    thumburl = getattr(settings, 'KEPTAR_URL', '/media') + thumbname[len(settings.KEPTAR_ROOT):]

    return thumburl


def generate_thumbnail(file, thumbname, size):
    image = Image.open(file)
    image.thumbnail(size)
    image.save(thumbname, image.format)


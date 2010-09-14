from django.conf import settings
import os, os.path
import Image

class AccessDenied(Exception):
    pass

class FileNotFound(Exception):
    pass

class NotDirectory(Exception):
    pass

def get_filelist(path):
    """Visszaadja a ``path`` konyvtarban levo konyvtarak es fileok listajat.
    A ``path`` a ``settings.KEPTAR_ROOT``-hoz relativ.
    A konyvtarak es a fileok listajat ket kulon listaban adja vissza.
    A ``settings.KEPTAR_EXTENSIONS``-nel allithatoak a tamogatott 
    kiterjesztesek.
    """

    abspath = os.path.abspath(os.path.join(settings.KEPTAR_ROOT, path))
    print abspath
    # vajon a celkonyvtar valoban a root-on belul talalhato? - /../... miatt
    if not abspath.startswith(settings.KEPTAR_ROOT):
        raise AccessDenied(abspath)
    
    if not os.path.isdir(abspath):
        raise NotDirectory(abspath)

    dirs = []
    pictures = []

    for fname in os.listdir(abspath):
        file = os.path.join(abspath, fname)
        if os.path.isdir(file):
            dirs.append(fname)
        if os.path.isfile(file):
            print file
            # a kiterjesztes tamogatott-e
            ext = file[file.rfind('.')+1:]
            if ext.lower() in settings.KEPTAR_EXTENSIONS:
                pictures.append(fname)

    return dirs, pictures

def get_thumbnail(file, regenerate=False):
    """Visszaadja, illetve ha nem letezik, akkor legeneralja a ``file``-hoz
    tartozo thumbnailt.
    Ha a ``regenerate`` ``True``, akkor ujrageneralja a thumbnailt.
    """

    ext = file[file.rfind('.')+1:]
    if not os.path.isfile(file) or ext.lower() not in settings.KEPTAR_EXTENSIONS:
        raise FileNotFound(file)
    
    basename = os.path.basename(file)
    dirname = os.path.dirname(file)
    thumbname = os.path.join(dirname, settings.KEPTAR_THUMBDIR, basename)
    if regenerate or not os.path.isfile(thumbname):
        if not os.path.isdir(os.path.dirname(thumbname)):
            os.mkdir(os.path.dirname(thumbname))
        generate_thumbnail(file, thumbname)
    
    return thumbname

def generate_thumbnail(file, thumbname):
    image = Image.open(file)
    image.thumbnail(settings.KEPTAR_THUMBSIZE)
    image.save(thumbname, image.format)


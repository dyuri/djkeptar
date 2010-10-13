from django.conf import settings
from django.core.urlresolvers import reverse
from keptar.utils import get_filelist, get_abspath, get_parent, enrich
from keptar.models import PBlogEntry
from keptar.forms import PBlogEntryForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseForbidden, HttpResponseRedirect

def listdir(request, path=""):
    """konyvtarlista megjelenitese"""

    # rossz eleresi ut, vagy "trukkozes" eseten hiba
    try:
        files = get_filelist(path)
    except:
        return HttpResponseForbidden('Access Forbidden')

    return render_to_response('listdir.html', {
        'path':     path,
        'parent':   get_parent(path),
        'files':    files,
        }, context_instance = RequestContext(request))


def showfile(request, fname):
    """egy adott kep megjelenitese"""

    # TODO: itt lehet csak valami kisebb felbontasu kepet kene mutatni

    # rossz eleresi ut, vagy "trukkozes" eseten hiba
    try:
        abspath = get_abspath(fname)
        fdata = enrich([fname])[fname]
    except:
        return HttpResponseForbidden('Access Forbidden')
    
    # ha be van lepve valaki, akkor beteheti a kepet a photoblogba
    if request.user.is_authenticated:
        try:
            # ha az elem mar szerepel az adatbazisban, akkor a formban az o
            # adatait szeretnenk latni
            form = PBlogEntryForm(instance=PBlogEntry.objects.get(path=fname))
        except PBlogEntry.DoesNotExist:
            # ha nem szerepel, akkor uj, ures formot szeretnenk
            form = PBlogEntryForm(initial={'path': fname})
    else:
        form = None

    return render_to_response('showfile.html', {
        'pbform': form,
        'parent': get_parent(fname),
        'fname': fname,
        'fdata': fdata,
        }, context_instance = RequestContext(request))


def submitpbentry(request):
    """kep betetele photoblogba
    illetve ha mar szerepel ott, akkor az adatainak megvaltoztatasa
    """

    # ha nincs belepve, akkor nem szabad
    # NOTE: @login_required dekoratorral szebb lenne, csak kene belepteto oldal
    if not request.user.is_authenticated:
        return HttpResponseForbidden('Access Forbidden')
    try:
        # ha az adott kep mar szerepel az adatbazisban, akkor az o adatait
        # szeretnenk frissiteni
        f = PBlogEntryForm(request.POST, 
                instance=PBlogEntry.objects.get(path=request.POST['path']))
    except PBlogEntry.DoesNotExist:
        # ha nem szerepel, akkor uj elemet hozunk letre a form alapjan
        f = PBlogEntryForm(request.POST)

    # ha a felhasznalot nem raknank hozza, akkor siman menthetnkenk,
    # igy viszont kulon kell menteni a kapcsolodo adatokat is (tag)
    pbe = f.save(commit=False)
    pbe.user = request.user
    pbe.save()
    f.save_m2m()

    return HttpResponseRedirect(reverse('showfile', args=[pbe.path]))


def pblog(request, id=None, slug=None):
    """photoblog bejegyzes megjelenitese"""
    try:
        # ha az id nincs megadva, akkor a legutolsot jelenitjuk meg
        if id is None:
            pbe = PBlogEntry.objects.latest('mark_date')
        else:
            pbe = PBlogEntry.objects.get(pk=id)
    except PBlogEntry.DoesNotExist:
        # hibas id volt megadva, vagy nincs meg bejegyzes
        return render_to_response('pblog.html', 
            {}, 
            context_instance = RequestContext(request))

    # elozo es kovetkezo elem meghatarozasa
    next = PBlogEntry.objects.filter(mark_date__gt=pbe.mark_date).order_by('mark_date')[:1]
    # python 2.6+
    # next = next if next else None
    if next:
        next = next[0]
    prev = PBlogEntry.objects.filter(mark_date__lt=pbe.mark_date).order_by('-mark_date')[:1]
    if prev:
        prev = prev[0]

    return render_to_response('pblog.html', {
        'pbe': pbe,
        'next': next,
        'prev': prev,
        }, context_instance = RequestContext(request))


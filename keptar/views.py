from django.conf import settings
from django.core.urlresolvers import reverse
from keptar.utils import get_filelist, get_abspath, get_parent, enrich
from keptar.models import PBlogEntry
from keptar.forms import PBlogEntryForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseForbidden, HttpResponseRedirect

def listdir(request, path=""):
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
    try:
        abspath = get_abspath(fname)
        fdata = enrich([fname])[fname]
    except:
        return HttpResponseForbidden('Access Forbidden')
    
    if request.user.is_authenticated:
        try:
            form = PBlogEntryForm(instance=PBlogEntry.objects.get(path=fname))
        except PBlogEntry.DoesNotExist:
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
    if not request.user.is_authenticated:
        return HttpResponseForbidden('Access Forbidden')
    try:
        f = PBlogEntryForm(request.POST, 
                instance=PBlogEntry.objects.get(path=request.POST['path']))
    except PBlogEntry.DoesNotExist:
        f = PBlogEntryForm(request.POST)
    pbe = f.save(commit=False)
    pbe.user = request.user
    pbe.save()
    f.save_m2m()

    return HttpResponseRedirect(reverse('showfile', args=[pbe.path]))


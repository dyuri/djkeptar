from django.conf import settings
from keptar.utils import get_filelist, get_abspath, enrich
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseForbidden

def listdir(request, path=""):
    try:
        files = get_filelist(path)
    except:
        raise
        return HttpResponseForbidden('Access Forbidden')

    return render_to_response('listdir.html', {
        'path':     path,
        'files':    files,
        }, context_instance = RequestContext(request))


def showfile(request, fname):
    try:
        abspath = get_abspath(fname)
        fdata = enrich([fname])[fname]
    except:
        raise
        return HttpResponseForbidden('Access Forbidden')

    return render_to_response('showfile.html', {
        'fname': fname,
        'fdata': fdata,
        }, context_instance = RequestContext(request))


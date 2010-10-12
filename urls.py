from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^/?$', 'keptar.views.listdir'),
    url(r'^list/(?P<path>.*)$', 'keptar.views.listdir', name='listdir'),
    url(r'^show/(?P<fname>.*)$', 'keptar.views.showfile', name='showfile'),
    url(r'^submitpbe$', 'keptar.views.submitpbentry', name='submitpbentry'),
    url(r'^admin/', include(admin.site.urls)),

    # media files
    url(r'media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)

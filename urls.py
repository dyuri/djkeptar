from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^/?$', 'keptar.views.listdir'),
    (r'^list/(?P<path>.*)$', 'keptar.views.listdir'),
    (r'^show/(?P<fname>.*)$', 'keptar.views.showfile'),
    (r'^admin/', include(admin.site.urls)),
)

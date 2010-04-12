from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', include('is303.apps.distributed.urls')),
    (r'^admin/', include(admin.site.urls)),
)

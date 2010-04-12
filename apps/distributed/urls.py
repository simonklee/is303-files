from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

import views as distributed_views

urlpatterns = patterns('',
    url(r'^$', direct_to_template,
    {'template': 'distributed/index.html'}),
    
    url(r'^upload_simple/$', distributed_views.simple,
    kwargs = {'template_name': 'distributed/distributed_simple.html'},
    name = 'distributed_simple')
)    
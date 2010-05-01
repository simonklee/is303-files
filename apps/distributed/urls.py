from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

import views as distributed_views

urlpatterns = patterns('',
    
    url(r'^$', distributed_views.index,
        {'template_name': 'distributed/index.html'},
        name= 'index'
    ),
    
    url(r'^upload_simple/$', distributed_views.simple,
        kwargs = {'template_name': 'distributed/distributed_simple.html'},
        name = 'distributed_simple'
    ),
    
    url(r'^tasks/suspend/(?P<task_id>(.*))/$', distributed_views.suspend_task_get,
        kwargs = {'template_name': 'distributed/distributed_suspend.html'},
        name = 'suspend_task_get'),
    
    url(r'^tasks/suspend/$', distributed_views.suspend_task,
        kwargs = {'template_name': 'distributed/distributed_suspend.html'},
        name = 'suspend_task'),
    
    url(r'^tasks/test/$', distributed_views.test,
        kwargs = {'template_name': 'distributed/distributed_test.html'},
        name = 'suspend_test'),
)

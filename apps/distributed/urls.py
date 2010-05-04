from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

import views as distributed_views


urlpatterns = patterns('',
    url(r'^$', direct_to_template,
        kwargs = {'template': 'distributed/index.html'},
        name = 'index'
    ),
    url(r'^upload_simple/$', distributed_views.simple,
        kwargs = {'template_name': 'distributed/distributed_simple.html'},
        name = 'distributed_simple'
    ),
    url(r'^tasks/test/$', direct_to_template,
        kwargs = {'template': 'distributed/distributed_test.html'},
        name = 'suspend_test'
    ),
    url(r'^tasks/upload/$', distributed_views.video_upload,
        name = 'video_upload'
    ),
    url(r'^tasks/video/(?P<video_id>\d+)/$', distributed_views.video_get,
        name = 'video_get'
    ),
    url(r'^tasks/video/$', distributed_views.video,
        kwargs = {'template_name': 'distributed/distributed_upload.html'},
        name = 'video'
    ),
    url(r'^tasks/suspend/apply/$', distributed_views.suspend_task,
        name = 'suspend_task'
    ),
    url(r'^tasks/suspend/(?P<task_id>(.*))/$', distributed_views.suspend_task_get,
        name = 'suspend_task_get'
    ),
    url(r'^tasks/suspend/$', direct_to_template,
        kwargs = {'template': 'distributed/distributed_suspend.html'},
        name = 'suspend'
    ),
)

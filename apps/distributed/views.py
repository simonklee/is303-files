import os

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.core.files import File

from celery.result import AsyncResult
from celery.backends import default_backend
from anyjson import serialize as JSON_dump

from apps.distributed.models import Video
from apps.distributed.forms import FilesForm, VideoForm
from apps.distributed.tasks import suspend, Convert
from settings import MEDIA_ROOT


def simple(request, template_name, **kwargs):
    '''Simple file upload view.'''
    #request.upload_handlers.insert(0, ProgressUploadHandler())

    if request.method == 'POST':
        form = FilesForm(request.POST, request.FILES)
        message = 'invalid'
        if form.is_valid():
            message = 'Form was valid!'
    else:
        form = FilesForm()
        message = 'Submit the form'
        
    return render_to_response(template_name, {'form': form, 'message': message },
                              context_instance=RequestContext(request))

def video_upload(request, **kwargs):
    '''Upload a video, and start processing the video in a background task.
    Returns the task_id for the background process.
    '''
    video = None
    response_data = dict()    
    form = VideoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        video = form.save()
    elif 'test-file1' in request.POST:
        try:
            with open(os.path.join(MEDIA_ROOT, request.POST['test-file1'])) as fp:
                video = Video()
                video.file = File(fp)
                video.save()
        except IOError:
            pass
    if video:
        res = Convert().apply_async(args=[video.id])
        response_data.update({
            'task_id': res.task_id,
            'status': u'PENDING',
        })
    return HttpResponse(JSON_dump(response_data), mimetype="application/json")
    
def video(request, **kwargs):
    #try:
    #    response_data.update({'latest': Video.converts.latest()})
    #except Video.DoesNotExist:
    #    pass
    response_data = dict({'form': VideoForm()})
    return render_to_response(kwargs.get('template_name'), response_data,
                              context_instance=RequestContext(request))

def video_get(request, video_id):
    response_data = dict();
    try:
        video = Video.objects.get(pk=video_id)
        response_data.update({
            'video_url': video.file.url,
            'video_date': video.uploaded.strftime('%Y-%m-%dT%H:%M:%S'),
            'video_id': video.id,
            'video_name': os.path.split(video.file.name)[1]
        })
    except Video.DoesNotExist:
        pass
    return HttpResponse(JSON_dump(response_data), mimetype="application/json")

def suspend_task(request):
    '''A view which executes a the ``suspend`` time task.'''
    kwargs = {'time': 5.0}
    if 'time' in request.GET:
        kwargs.update({'time': float(request.GET['time'])})
    res = suspend.apply_async(kwargs=kwargs)
    response_data = {'task_id': res.task_id, 'status':u'PENDING'}
    return HttpResponse(JSON_dump(response_data), mimetype="application/json")
    
def suspend_task_get_block(request, task_id):
    '''A function which invokes a blocking status update for a given task.'''
    res = default_backend.wait_for(task_id)
    status = default_backend.get_status(task_id)
    data = dict(task_id=task_id, status=status)
    return HttpResponse(JSON_dump(data), mimetype="application/json")

def suspend_task_get(request, task_id):
    '''Returns status and result formattet in JSON.'''
    status = default_backend.get_status(task_id)
    res = default_backend.get_result(task_id)
    response_data = dict(task_id=task_id, status=status, result=res)
    if status in default_backend.EXCEPTION_STATES:
        traceback = default_backend.get_traceback(task_id)
        response_data.update({
            'traceback': traceback,
            'result': str(res.args[0])
        })
    return HttpResponse(JSON_dump(response_data), mimetype="application/json")

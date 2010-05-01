from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponse

from celery.result import AsyncResult
from celery.backends import default_backend
from anyjson import serialize as JSON_dump

from apps.distributed import ProgressUploadHandler
from apps.distributed.models import Files
from apps.distributed.forms import FilesForm
from apps.distributed.tasks import add, suspend

def index(request, template_name):
        
    return render_to_response(template_name, {},
                              context_instance=RequestContext(request))

def simple(request, template_name, **kwargs):
    '''
    simple file upload view.
    
    '''
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

def test(request, template_name=None, **kwargs):
    return render_to_response(template_name, {},
                              context_instance=RequestContext(request))

def suspend_task(request, template_name=None, **kwargs):
    '''
    A view which executes a task.
    '''
    time = 5.0
    if 'time' in request.GET:
        time = float(request.GET['time'])
    res = suspend.apply_async(args=[time])
    response_data = {'task_id': res.task_id, 'status':u'PENDING'}
    
    if 'json' in request.GET:
        return HttpResponse(JSON_dump(response_data), mimetype="application/json")
    else:
        return render_to_response(template_name, response_data,
                              context_instance=RequestContext(request))
    
def suspend_task_get_block(request, task_id, template_name=None, **kwargs):
    '''
    A function which invokes a blocking status update for a given task
    
    '''
    res = default_backend.wait_for(task_id)
    status = default_backend.get_status(task_id)
    data = dict(task_id=task_id, status=status)
    return HttpResponse(JSON_dump(data), mimetype="application/json")

def suspend_task_get(request, task_id, template_name=None, **kwargs):
    '''
    A function which returns a update based on the status of a given task.
    
    '''
    status = default_backend.get_status(task_id)
    res = default_backend.get_result(task_id)
    data = dict(task_id=task_id, status=status)
    return HttpResponse(JSON_dump(data), mimetype="application/json")
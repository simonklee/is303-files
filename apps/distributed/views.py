
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from models import Files
from forms import FilesForm
from apps.distributed import ProgressUploadHandler

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
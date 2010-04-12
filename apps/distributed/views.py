
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from models import Files
from forms import FilesForm

def simple(request, template_name, **kwargs):
    '''
    simple file upload view.
    
    '''
    if request.method == 'POST':
        form = FilesForm(request.POST, request.FILES)
        if form.is_valid():
            message = 'Form was valid!'
    else:
        form = FilesForm()
        message = 'invalid'
    return render_to_response(template_name, {'form': form, 'message': message },
                       context_instance=RequestContext(request))
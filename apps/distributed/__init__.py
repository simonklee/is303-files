from django.core.files.uploadhandler import FileUploadHandler
from django.core.cache import cache
from django.conf import settings

from jogging import logging

class ProgressUploadHandler(FileUploadHandler):
    '''
    A custom file upload handler with the aim to provide the user with
    feedback during file uploads.
    
    The ProgressUploadHandler can be called onthe fly by simply prioritizing it
    in the request.upload_handlers list  like this ::
    
        request.upload_handler.insert(0, ProgressUploadHandler())
        
    The ProgressUploadHandler is like a filter, which tracks some of the data
    passed to it, then passing the raw data onwards, without actually doing
    something. with it. 
    '''
    
    def __init__(self, request=None):
        '''
        Define fields used for tracking an upload. 
        '''
        super(ProgressUploadHandler, self).__init__(request)
        self.progress = 0
        self.progress_id = None
        self.cach_key = None

    def handle_raw_input(self, input_data, META, content_length, boundary,
                         encoding):
        '''
        Allows the handler to completely override the parsing of the raw
        HTTP input.

        ``input_data`` is a file-like object that supports read()-ing.

        ``META`` is the same object as request.META.

        ``content_length`` is the length of the data in input_data.

        ``boundary`` is the MIME boundary for this request.

        ``encoding`` is the encoding of the request.
        '''
        if 'progress-id' in self.request.GET and content_length > 0:
            self.progress_id = self.request.GET['progress-id']
        return None
    
    def new_file (self, field_name, file_name, content_type, content_length,
                  charset):
        '''
        Callback signaling that a new file upload is starting. This is called
        before any data has been fed to any upload handlers.
                
        ``field_name`` is a string name of the file <input> field.
        
        ``file_name`` is the unicode filename that was provided by the browser.
        
        ``content_type`` is the MIME type provided by the browser -- E.g.
        'image/jpeg'.
        
        ``content_length`` is the length of the image given by the browser.
        Sometimes this won't be provided and will be None., None otherwise.
        
        ``charset`` is the character set (i.e. utf8) given by the browser.
        Like content_length, this sometimes wonn't be provided.
        '''
        if self.progress_id:
            self.cach_key = '%s_%s_%s' % (self.request.META['REMOTE_ADDR'],
                self.progress_id, field_name)
            cache.set(self.cach_key, 0, 360)
    
    def recieve_data_chunk(self, raw_data, start):
        '''
        Receives a "chunk" of data from the file upload.
        
        ``raw_data is`` a byte string containing the uploaded data.
        
        ``start`` is the position in the file where this raw_data chunk begins.

        The data you return will get fed into the subsequent upload handlers'
        receive_data_chunk methods. In this way, one handler can be a "filter"
        for other handlers.
        
        Return None from receive_data_chunk to sort-circuit remaining upload
        handlers from getting this chunk.. This is useful if you're storing
        the uploaded data yourself and don't want future handlers to store
        a copy of the data.
        
        If you raise a StopUpload or a SkipFile exception, the upload will
        abort or the file will be completely skipped.
        '''
        self.progress += self.chunk_size
        if self.cach_key:
            try:
                percent = min(100, int(100 * self.progress / self.content_length))
                cache.incr(self.cach_key, percent)
            except ValueError, e:
                logging.error('Tried to increment a non-existing cache-key;\
                              %s %s' % (self.cach_key, e)) 
                
        return raw_data
        
    def file_complete(self, file_size):
        '''
        return None to indicate that the UploadedFile object should come from
        subsequent upload handlers.
        '''
        return None
    
    def upload_complete(self):
        '''
        Callback signaling that the entire upload (all files) has completed.
        '''
        if settings.DEBUG:
            logging.debug('Upload for %s and %s was completed'
                          % (self.field_name, self.cach_key))
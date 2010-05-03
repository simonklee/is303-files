A short look at handlers
--------------------------



**djangodocs urls**

Overview of relevant links in django docs.

    *   `File uploads <http://docs.djangoproject.com/en/dev/topics/http/file-uploads/#upload-handlers>`_
        is a document describing how django handles file uploads with focus on
        forms, views, where files are stored and the upload handler.
    
    *   `HttpRequest.FILES <http://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpRequest.FILES>`_
        is similar to PHP's $_FILES.
    
    *   `FileField (and ImageField) <http://docs.djangoproject.com/en/dev/ref/models/fields/#filefield>`_
        are the model representation for files. They require some extra
        attention; `upload_to` must be defined.
    
    *   `Managing files <http://docs.djangoproject.com/en/dev/topics/files/>`_
        describes the access APIs for files. It discusses the `File` object and
        the use of file storage objects.
    
    *   `File storage API <http://docs.djangoproject.com/en/dev/ref/files/storage/#ref-files-storage>`_
    
    *   `Binding uploaded files to a form <http://docs.djangoproject.com/en/dev/ref/forms/api/#binding-uploaded-files>`_
        deals with how to send and encode forms which contain uploaded files.
    
    *   `Writing a custom storage system <http://docs.djangoproject.com/en/dev/howto/custom-file-storage/#howto-custom-file-storage>`_
        short discussion on how to write a custom storage system. 
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Files(models.Model):
    '''
    A simple file storage model which handles some information about files
    uploaded to the server.
    
    '''
    file = models.FileField(_('file'), upload_to='upload')
    uploaded = models.DateField(_('time uploaded'), auto_now_add=True)


class Video(models.Model):
    '''A model used to store video-files.'''
    video = models.FileField(_('video'), upload_to='upload/video')
    uploaded = models.DateField(_('time uploaded'), auto_now_add=True)
    converted = models.FileField(_('converted video'),
                                 upload_to='upload/converted_video',
                                 blank=True, null=True)
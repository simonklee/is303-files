from django.db import models
from django.utils.translation import ugettext_lazy as _


class Files(models.Model):
    '''
    A simple file storage model which handles some information about files
    uploaded to the server.
    
    '''
    file = models.FileField(_('file'), upload_to='upload')
    uploaded = models.DateField(_('time uploaded'), auto_now_add=True)


class VideoManagerConverted(models.Manager):
    def get_query_set(self):
        return super(VideoManagerConverted, self).get_query_set().filter(converted=True)


class VideoManager(models.Manager):
    def get_query_set(self):
            return super(VideoManager, self).get_query_set()


class Video(models.Model):
    '''A model used to store video-files.'''
    file = models.FileField(_('video'), upload_to='upload/video')
    #file_converted = models.FileField(_('converted video'),
    #                             upload_to='upload/converted_video',
    #                             blank=True, null=True)
    uploaded = models.DateTimeField(_('time uploaded'), auto_now_add=True)
    converted = models.BooleanField(_('converted'), default=False)
    objects = VideoManager()
    converts = VideoManagerConverted()
    
    def __unicode__(self):
        return u'%s' % self.file_converted
    
    class Meta:
        get_latest_by = 'uploaded'

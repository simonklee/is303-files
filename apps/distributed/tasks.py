import time as ctime
import os
import subprocess
import shlex
import pdb

from celery.task import Task
from celery.decorators import task
from celery.registry import tasks
from django.core.files import File
from magic import Magic
from jogging import logging

from apps.distributed.models import Video 

@task()
def add(x, y):
    return x + y

@task()
def suspend(time):
    '''Suspend the task for x seconds.'''
    ctime.sleep(time)
    return True


class Convert(Task):
    def run(self, video_id, **kwargs):
        '''``video_id`` should be the video-object which is converted.
        
        **ffmpeg one-pass CRF**:
        .. code-block:: bash
        
            $ ffmpeg -i input.mov -acodec libfaac -ab 128k -ac 2 -vcodec libx264 \
            -vpre slow -crf 22 -threads 0 output.mp4
        
        **ffmpeg two-pass fast**:
        .. code-block:: bash
        
            ffmpeg -i input.avi -pass 1 -vcodec libx264 -vpre fast_firstpass \
            -b 512k -bt 512k -threads 0 -f rawvideo -an -y /dev/null
            
            ffmpeg -i input.avi -pass 2 -acodec libfaac -ab 128k -ac 2 \
            -vcodec libx264 -vpre fast -b 512k -bt 512k -threads 0 output.mp4
        '''
        #pdb.set_trace()
        try:
            self.video = Video.objects.get(pk=video_id)
        except Video.DoesNotExist, e:
            self.retry(args=[video_id], kwargs=kwargs,
                       options={'exc':exc, 'countdown':2})
        if not os.path.exists(self.video.file.path):
            raise ValueError()
        self.tmp_file = '.'.join([self.video.file.path.rsplit('.', 1)[0], 'mp4'])
        ffmpeg = ['ffmpeg',
                  '-i', self.video.file.path,
                  '-acodec', 'libfaac',
                 '-ab', '128k',
                 '-ac', '2',
                 '-vcodec', 'libx264',
                 '-vpre', 'slow',
                 '-crf', '22',
                 '-threads', '0',
                 self.tmp_file]
    
        ret = subprocess.call(ffmpeg)
        if ret != 0 or not os.path.exists(self.tmp_file):
            logging.error('Conversion error, ffmpeg returned %s' % ret)
            raise OSError()
        else:
            self._move_moov_atoms()
            self._save_cleanup()
            return True
        return False

    def _save_cleanup(self):
        '''Save and cleanup.'''
        self.video.file.delete()
        with open(self.tmp_file) as fp:
            self.video.file_converted = File(fp)
            self.video.converted = True
            self.video.save()
        os.remove(self.tmp_file)
    
    def _move_moov_atoms(self):
        '''Server needs the H264 file to have its moov atoms (or boxes) in front
        of the data. The qt-faststart.c program - shipped with FFMpeg - rewrites
        H264 files so their atoms are placed in the required order. This is only
        necessary to do if it's a quicktime file.
        
        ``file_path`` should be a path to the file-object which will be converted.
        
        $ qt-faststart <infile.mov> <outfile.mov>
        '''
        magic = Magic(mime=True)
        if 'video/quicktime' is magic.from_file(self.tmp_file):    
            print "mime-type was quicktime \n"
            subprocess.call(["qt-faststart", self.tmp_file, self.tmp_file])

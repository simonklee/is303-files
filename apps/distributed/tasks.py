import time as ctime
import os
import shutil
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
        '''``video_id`` is the id for the video which is converted.'''
        #pdb.set_trace()
        try:
            self.video = Video.objects.get(pk=video_id)
        except Video.DoesNotExist, e:
            self.retry(args=[video_id], kwargs=kwargs,
                       options={'exc':e, 'countdown':2})
        try:        
            (path, filename) = os.path.split(self.video.file.path)
            (name, ext) = os.path.splitext(filename)
            self.tmp_dir = self._mkdir(os.path.join(path, '_'.join([name, 'tmp'])))
            tmp_mp4 = os.path.join(self.tmp_dir, '.'.join([name, 'mp4']))
            tmp_mov = '.'.join([os.path.splitext(tmp_mp4)[0], ext])
            shutil.copyfile(self.video.file.path, tmp_mov)
            
            self._move_moov_atoms(tmp_mov)
            self._ffmpeg(tmp_mov, tmp_mp4)
            self._move_moov_atoms(tmp_mp4)
            self._save(tmp_mp4)
            return video_id
        finally:
            self._clean()

    def _clean(self):
        if os.path.exists(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)
    
    def _mkdir(self, path, **kwargs):
        if os.path.exists(path):
            shutil.rmtree(path)
        os.mkdir(path)
        return path
    
    def _save(self, file):
        '''Delete original file, save converted.'''
        self.video.file.delete()
        with open(file) as fp:
            self.video.file = File(fp)
            self.video.converted = True
            self.video.save()

    def _ffmpeg(self, in_file, out_file):
        '''**ffmpeg one-pass CRF**:
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
        ffmpeg = ['ffmpeg',
                  '-i', in_file,
                  '-acodec', 'libfaac',
                  '-ab', '128k',
                  '-ac', '2',
                  '-vcodec', 'libx264',
                  '-vpre', 'slow',
                  '-crf', '22',
                  '-threads', '0',
                  out_file]
        ret = subprocess.call(ffmpeg)
        if ret != 0 or not os.path.exists(out_file):
            logging.error('Conversion error, ffmpeg returned %s' % ret)
            raise OSError()
        return out_file

    def _move_moov_atoms(self, in_file):
        '''Server needs the H264 file to have its moov atoms (or boxes) in front
        of the data. The qt-faststart.c program - shipped with FFMpeg - rewrites
        H264 files so their atoms are placed in the required order. This is only
        necessary to do if it's a quicktime file.
        
        $ qt-faststart <infile.mov> <outfile.mov>
        '''
        moovs = (
            'video/x-ms-asf',
            'video/quicktime',
            'application/octet-stream',
        )
        magic = Magic(mime=True)
        if magic.from_file(self.video.file.path) in moovs:
            (name, ext) = os.path.splitext(in_file)
            tmp = ''.join([name, '_tmp', ext])
            shutil.copyfile(in_file, tmp)
            ret = subprocess.call(["qt-faststart", tmp, in_file])
            if ret != 0:
                raise OSError()

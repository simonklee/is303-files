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

from apps.distributed.models import Video 

@task()
def add(x, y):
    return x + y

@task()
def suspend(time):
    '''Suspend the task for x seconds.'''
    ctime.sleep(time)
    return True

#@task()
def compress(video_id):
    '''``video_id`` should be the id for the video-object which is converted.
    Returns the video_id when done.
    
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
    pdb.set_trace()
    video = Video.objects.get(pk=long(video_id))
    video.file_converted = File(video.file)
    video.save()
    print "copied \"%s\" > \"%s\"" % (video.file, video.file_converted)
        
    # If quicktime file we need to call extra bit routines on the file.
    magic = Magic(mime=True)
    mime_type = magic.from_file(video.file.path)
    is_quicktime = True if 'video/quicktime' is mime_type else False
    print "mime-type was %s and quicktime is %s" % (mime_type, is_quicktime)
    
    out_path = '.'.join([video.file_converted.path.rsplit('.', 1)[0], 'mp4'])
    print "out_path is \"%s\"" % out_path
    
    ffmpeg = ['ffmpeg',
              '-i', video.file_converted.path,
              '-acodec', 'libfaac',
             '-ab', '128k',
             '-ac', '2',
             '-vcodec', 'libx264',
             '-vpre', 'slow',
             '-crf', '22',
             '-threads', '0',
             out_path]
    print "ffmpeg command's: \"$ %s\"" % ffmpeg
    
    subprocess.call(ffmpeg)
    if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
        video.file_converted.delete()
        print "cp deleted was a %s" % \
            ('success' if video.file_converted is None else 'faliure')
        with open(out_path) as fp:
            video.file_converted = File(fp)
            video.save()
        print "video was converted and saved at %s" % video.file_converted
    return video.id

def move_moov_atoms(file_path):
    '''Server needs the H264 file to have its moov atoms (or boxes) in front
    of the data. The qt-faststart.c program - shipped with FFMpeg - rewrites
    H264 files so their atoms are placed in the required order. This is only
    necessary to do if it's a quicktime file.
    
    ``file_path`` should be a path to the file-object which will be converted.
    
    $ qt-faststart <infile.mov> <outfile.mov>
    '''
    if os.path.exists(file_path):
        subprocess.call("qt-faststart", file_path, file_path)

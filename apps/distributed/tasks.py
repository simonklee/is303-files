import time as ctime

from celery.task import Task
from celery.decorators import task
from celery.registry import tasks


@task()
def add(x, y):
    return x + y


@task()
def suspend(time):
    '''
    Suspend the task for x seconds. A testing method used to play with asynchrous
    calls to a task.
    '''
    ctime.sleep(time)
    return True

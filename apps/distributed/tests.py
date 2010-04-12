from django.core.urlresolvers import reverse
from django.test import TestCase
from django.conf import settings
from django.test.simple import run_tests as run_tests_orig
from django.test.simple import DjangoTestSuiteRunner

from apps.distributed.tasks import add, suspend

class AddTaskTest(TestCase):
        
    def test_addition(self):
        '''
        Test our simple addition client
        '''
        res = add.delay(6, 14)
        self.assertEquals(res.get(), 20)
        self.assertTrue(res.successful())
    
    def test_states(self):
        '''
        Test the different states of a response.
        '''
        res = add.delay(1, 1)
        self.assertEquals(res.get(), 2)

class SuspendTaskTest(TestCase):
    
    def test_suspend(self):
        '''
        Suspend will cause a delay in the worker task.
        '''
        res = suspend.delay(1.0) # one sec
        self.assertEquals(res.get(), True)
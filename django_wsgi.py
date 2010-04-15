import os
import sys
import site
import django.core.handlers.wsgi

apache_configuration= os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(workspace) 
site.addsitedir('/home/acopy/django/is303/ve/lib/python2.6/site-packages')
sys.path.append('/home/acopy/django/is303')

# Set the django settings and define the wsgi app
os.environ['DJANGO_SETTINGS_MODULE'] = 'is303.settings'
application = django.core.handlers.wsgi.WSGIHandler()

# Mount the application to the url
applications = {'/':'application', }

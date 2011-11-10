import os
import sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'project.settings'
os.environ['PATH'] = '/home/dotcloud/env/bin:%s' % os.environ['PATH']
os.environ['GEM_HOME'] = '/home/dotcloud/env'
import django.core.handlers.wsgi
djangoapplication = django.core.handlers.wsgi.WSGIHandler()
def application(environ, start_response):
    if 'SCRIPT_NAME' in environ:
        del environ['SCRIPT_NAME']
    return djangoapplication(environ, start_response)


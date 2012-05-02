import os, sys
sys.path.append('/home/ville/areareservation/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'areareservation/settings.py'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


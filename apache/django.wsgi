import os
import sys

sys.path.append('/home/ville/areareservation')
sys.path.append('/home/ville/areareservation/areareservation')

os.environ['DJANGO_SETTINGS_MODULE'] = 'areareservation.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


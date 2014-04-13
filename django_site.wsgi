import os
import sys
sys.path = ['/var/www/switch_idea'] + sys.path
os.environ['DJANGO_SETTINGS_MODULE'] = 'switch_idea.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


#!/usr/bin/env python2
import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'observatory.settings'


path = '/var/www/Observatory'
if path not in sys.path:
    sys.path.append(path)

path = '/var/www/Observatory/observatory/'
if path not in sys.path:
    sys.path.append(path)

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()


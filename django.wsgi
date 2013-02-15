import os
import sys

#sys.path.append('/root/Meeting-scheduler/wai')
sys.path.append('/var/www/wai.few.vu.nl')
#sys.path.append('/root/Meeting-scheduler/')
#sys.path.append('/var/www/wai.few.vu.nl/appli')
#sys.path.append('/root/Meeting-scheduler')
#sys.path.append('/root/Meeting-scheduler/wai/scheduler')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

from django.conf.urls.defaults import *

from django.conf import settings

# Enable the admin
from django.contrib import admin
admin.autodiscover()

# Register to databrowse
#from django.contrib import databrowse
#from wai.scheduler.models import Group,Presenter,Room,Meeting,Presentation
#databrowse.site.register(Meeting)
#databrowse.site.register(Presentation)
#databrowse.site.register(Presenter)
#databrowse.site.register(Group)
#databrowse.site.register(Room)

from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
	(r'^$', 'wai.scheduler.views.index'),
	(r'^page/', include('wai.scheduler.urls')),
#	(r'^browse/(.*)', databrowse.site.root),
	(r'^admin/(.*)', admin.site.root),
	(r'^accounts/login/$', login, {'template_name': 'wai/login.html'}),
	(r'^accounts/logout/$', logout, {'template_name': 'wai/logout.html'}),
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT})
)

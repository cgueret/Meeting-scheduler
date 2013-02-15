from django.conf.urls.defaults import *

urlpatterns = patterns('wai.scheduler.views',
   # Index
   (r'^$', 'index'),
   
   # Presentations
   (r'^presentation/$', 'presentations'),
   (r'^presentation/(?P<presentation_id>\d+)/$', 'presentation_detail'),
   
   # Agenda
   (r'^schedule/$', 'schedules'),
   (r'^schedule/(?P<year>\d+)/$', 'schedule_year'),
   (r'^schedule/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', 'meeting'),

   # Groups
   (r'^group/$', 'groups'),
   (r'^group/(?P<group_id>\d+)/$', 'group_detail'),
   
   # Presenters
   (r'^presenter/$', 'presenters'),
   (r'^presenter/(?P<presenter_id>\d+)/$', 'presenter_detail'),

   # ICAL export
   (r'^ical/schedule.ics$', 'schedule_ics'),

   # Mails export
   (r'^mails.txt$', 'raw_mails'),
   
   # Mailing export
   (r'^mailing/send_request/$', 'send_request'),
   (r'^mailing/send_announce/$', 'send_announce'),
)


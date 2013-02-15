import atom.service
import gdata.service
import gdata.calendar
import gdata.calendar.service
from datetime import datetime,timedelta

PUB_LINK = '/calendar/feeds/sveua2ct2tem1s3n7rstb2rec8@group.calendar.google.com/private/full'
class GoogleExport(object):
	def __init__(self, **kwargs):
		# Connect to the calendar service
		self.calendar_service = gdata.calendar.service.CalendarService()
		self.calendar_service.email = 'christophe.gueret@gmail.com'
		self.calendar_service.password = ''
		self.calendar_service.source = 'VU-WAI_meeting_exporter-0.1'
		self.calendar_service.ProgrammaticLogin()

		# Generate the relevant content
		self._meeting = kwargs['instance'].meeting
		self._title = "WAI meeting : %s" % self._meeting.presenters()
		self._where = self._meeting.location.name
		self._content = ""
		for pres in self._meeting.presentation_set.all():
			self._content = "%s<b>%s : %s</b><br/>%s<br/><br/>" % (self._content, pres.presenter.name, pres.title, pres.abstract)

		# Was it created or modified ?
		self._is_new = kwargs['created']
		
	def publish_meeting(self):
		event = None
		
		if (self._is_new):
			# Create a new event
			event = gdata.calendar.CalendarEventEntry()
			start = "%sT11:00:00" % self._meeting.date
			end   = "%sT12:00:00" % self._meeting.date
			event.when.append(gdata.calendar.When(start_time=start, end_time=end))
		else:
			# Find the event in Gcalendar
			event = self._find_event()

		if event == None:
			raise "Error with this event"

		# Set the correct values
		event.title = atom.Title(text=self._title)
		event.content = atom.Content(text=self._content)
		event.where.append(gdata.calendar.Where(value_string=self._where))
		
		print event
		if (self._is_new):
			# Publish the event
			self.calendar_service.InsertEvent(event, PUB_LINK)
		else:
			# Update the event		
			self.calendar_service.UpdateEvent(event.GetEditLink().href, event)
		
	def delete_meeting(self):
		# Find the event in Gcalendar
		event = self._find_event()
		
		# Delete it
		self.calendar_service.DeleteEvent(event.GetEditLink().href)
		
	def _find_event(self):
		# Find the meeting object
		query = gdata.calendar.service.CalendarEventQuery('sveua2ct2tem1s3n7rstb2rec8@group.calendar.google.com', 'private', 'full')
		start_day = self._meeting.date.isoformat()
		end_day   = (self._meeting.date + timedelta(days=1)).isoformat()
		query.start_min = start_day
		query.start_max = end_day
		query.max_results=1
		feed = self.calendar_service.CalendarQuery(query)
		if len(feed.entry) == 0:
			raise "Meeting not found"
			
		return feed.entry[0]
	

import datetime
from django.db import models
from django import forms
#from django.template.loader import render_to_string
#from django.db.models.signals import post_save,pre_delete
#from google_export import GoogleExport

class Group(models.Model):
	name = models.CharField(max_length=100)
	def members_count(self):
		return self.presenter_set.all().count()
	def __unicode__(self):
		return self.name
	members_count.short_description = "Nb. of members"		


class Room(models.Model):
	name = models.CharField(max_length=50)
	note = models.CharField(max_length=100,blank=True)
	def __unicode__(self):
		return self.name


class Presenter(models.Model):
	name = models.CharField('Name', max_length=100)
	group = models.ForeignKey(Group)
	email = models.EmailField(blank=True)
	note = models.CharField(max_length=200,blank=True)
	available = models.BooleanField(default=True)
	
	class Meta:
		ordering = ['name']

	def __unicode__(self):
		return self.name
	
	def presentations_count(self):
		return self.presentation_set.all().count()
	presentations_count.short_description = 'Nb. of presentations'
	
	def last_presentation(self):
		if self.presentations_count() > 0:
			return self.presentation_set.order_by('-meeting')[0].meeting.date
		else:
			return 'None'
	last_presentation.short_description = 'Last presentation'


class Meeting(models.Model):
	date = models.DateField('Meeting date',primary_key=True)
	location = models.ForeignKey(Room)
	
	def days_offset(self):
		datediff = self.date - datetime.date.today()
		return datediff.days
	
	def __unicode__(self):
		return self.date.strftime("%d %B %Y")
		
	def is_today(self):
		return self.date() == datetime.date.today()
	
	def presenters(self):
		return ' and '.join([pres.presenter.name for pres in self.presentation_set.all()])
	presenters.short_description = 'List of presenters'

	
class Presentation(models.Model):
	meeting = models.ForeignKey(Meeting)
	presenter = models.ForeignKey(Presenter)
	slides = models.FileField(upload_to='slides',blank=True)
	title = models.CharField(max_length=200,blank=True)
	abstract = models.TextField(blank=True)
	def __unicode__(self):
		return self.presenter.name + ' (' + self.meeting.date.strftime("%d %B %Y") + ')'


class LoginForm(forms.Form):
	username = forms.CharField(max_length=100)
	password = forms.CharField(widget=forms.PasswordInput(render_value=False),max_length=100)
	
class SendAnnounceForm(forms.Form):
	subject = forms.CharField(max_length=200,widget=forms.TextInput)
	message = forms.CharField(widget=forms.Textarea)

class SendRequestForm(forms.Form):
	subject 	= forms.CharField(max_length=200,widget=forms.TextInput)
	message 	= forms.CharField(widget=forms.Textarea)
	identifier	= forms.DateField(widget=forms.HiddenInput)
	
#def presentation_save_handler(sender, **kwargs):
#	google_export = GoogleExport(**kwargs)
#	google_export.publish_meeting()
#	del google_export
	
#def meeting_delete_handler(sender, **kwargs):
#	google_export = GoogleExport(**kwargs)
#	google_export.delete_meeting()
#	del google_export
	
#post_save.connect(presentation_save_handler, sender=Presentation)
#pre_delete.connect(meeting_delete_handler, sender=Meeting)

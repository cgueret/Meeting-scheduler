from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from datetime import date, datetime
from wai.scheduler.models import Meeting, Presenter, Group, Presentation
from wai.scheduler.models import SendAnnounceForm, SendRequestForm
from django.template import RequestContext
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import iri_to_uri
from django.utils.http import urlquote_plus
from django.conf import settings
#import pytz
import vobject
from dateutil.tz import *
import operator
import logging

logging.basicConfig(
    level = logging.WARN,
    format = '%(asctime)s %(levelname)s %(message)s',
    filename = '/tmp/djangoLog.log',)


def index(request):
    year = datetime.now().year
    return HttpResponseRedirect("/page/schedule/%s" % year)
    
#    # Get all meetings
#    meetings_list = Meeting.objects.filter(date__lte=datetime.now()).order_by('-date')
    
    # Call the template
#    context = {
#        'meetings_list' : meetings_list,
#    }
#    return render_to_response('wai/index.html', context, context_instance=RequestContext(request))

def presentations(request):
    # Get the list of all presentations
    presentation_list = Presentation.objects.order_by('-meeting__date')

    # Set the context
    context = {
        'presentation_list' : presentation_list
    }

    return render_to_response('wai/presentations.html', context, context_instance=RequestContext(request))
    
def presentation_detail(request, presentation_id):
    # Get this presentation
    presentation = get_object_or_404(Presentation, id=presentation_id)
    
    # Get the list of all presentations by the same presenter
    presentation_list = get_list_or_404(Presentation, presenter=presentation.presenter)

    # Set the context
    context = {
        'presentation' : presentation,
        'presentation_list' : presentation_list
    }
    
    return render_to_response('wai/presentation_detail.html', context, context_instance=RequestContext(request))


def meeting(request, year, month, day):
    # Get this presentation
    dates = datetime(int(year), int(month), int(day))
    meeting = get_object_or_404(Meeting, date=dates)
    
    # Set the context
    context = {
        'date' : dates,
        'meeting' : meeting,
        'url' : request.build_absolute_uri(),
        'url2' : urlquote_plus(request.build_absolute_uri())
    }
    
    return render_to_response('wai/meeting.html', context, context_instance=RequestContext(request))

def groups(request):
    group_list = Group.objects.order_by('name')
    context = {
        'group_list' : group_list
    }
    return render_to_response('wai/groups.html', context, context_instance=RequestContext(request))
    
def group_detail(request, group_id):
    presenter_list = get_list_or_404(Presenter, group=group_id)
    context = {
        'presenter_list' : presenter_list,
        'group_name' : Group.objects.get(id=group_id).name
    }
    return render_to_response('wai/group_detail.html', context, context_instance=RequestContext(request))


def presenters(request):
    group_list = Group.objects.order_by('name')
    presenter_list = Presenter.objects.order_by('name')
    context = {
        'group_list' : group_list,
        'presenter_list' : presenter_list,
    }
    return render_to_response('wai/presenters.html', context, context_instance=RequestContext(request))
    
    
def presenter_detail(request, presenter_id):
    presenter = get_object_or_404(Presenter, id=presenter_id)
    presentation_list = presenter.presentation_set.all()

    context = {
        'presenter' : presenter,
        'presentation_list' : presentation_list
    }

    return render_to_response('wai/presenter_detail.html', context, context_instance=RequestContext(request))

    
def schedules(request):
    # Find first and last event
    first = Meeting.objects.order_by('date')[0]
    last = Meeting.objects.order_by('-date')[0]
    
    # Create the list of years and the presentations count
    years_list = {}
    for i in range(first.date.year, last.date.year + 1):
        years_list["%d" % i] = Meeting.objects.filter(date__year=i).count()
        
    context = {
        'years_list' : years_list,
    }
    
    return render_to_response('wai/schedules.html', context, context_instance=RequestContext(request))

def schedule_year(request, year):
    meetings_list = Meeting.objects.filter(date__year=year).order_by('date')
    for meeting in meetings_list:
        if meeting.days_offset() >= 0:
            meeting.nextMeeting = True
            break
    presenters = Presenter.objects.filter(available=True)
    presenter_list = list()
    for presenter in presenters:
        last = presenter.last_presentation()
        if last == 'None':
            last = date(1970, 1, 1)
        if last < date.today():
            presenter_list.append({'presenter':presenter, 'date':last})
        
    context = {
        'meetings_list' : meetings_list,
        'reserve_list' : sorted(presenter_list, key=operator.itemgetter('date')),
        'year' : year
    }
    
    return render_to_response('wai/schedule_year.html', context, context_instance=RequestContext(request))
    
def schedule_ics(request):
    meetings_list = Meeting.objects.order_by('date')
    
    #tz = pytz.timezone('Europe/Amsterdam')
    
    cal = vobject.iCalendar()
    cal.add('method').value = 'PUBLISH'  # IE/Outlook needs this
    
    for meeting in meetings_list:
        #date = datetime(meeting.date.year, meeting.date.month, meeting.date.day, tzinfo=zoneinfo('Europe/Amsterdam'))
        #date = datetime(meeting.date.year, meeting.date.month, meeting.date.day, tzinfo=tz)
	#date = datetime(meeting.date.year, meeting.date.month, meeting.date.day)
	date = datetime(meeting.date.year,meeting.date.month,meeting.date.day,0,0,0,0,gettz('Europe/Amsterdam'))
        vevent = cal.add('vevent')
        
        # UID
        vevent.add('uid').value = "WAI-%s@wai.few.vu.nl" % meeting.date
        
        # Begin and end
        vevent.add('dtstart').value = date.replace(hour=11)
        vevent.add('dtend').value = date.replace(hour=12)
        
        # Creation date
        vevent.add('dtstamp').value = datetime.utcnow()
        
        # Title, location and description
        vevent.add('summary').value = "WAI meeting : %s" % meeting.presenters()
        vevent.add('location').value = meeting.location.name
        text = ""
        for p in meeting.presentation_set.all():
            text += "%s : %s\n%s\n\n" % (p.presenter.name, p.title, p.abstract)
        vevent.add('description').value = text
        
    icalstream = cal.serialize()
    response = HttpResponse(icalstream, mimetype='text/calendar')
    response['Filename'] = 'export.ics'  # IE needs this
    response['Content-Disposition'] = 'attachment; filename=export.ics'

    return response

def raw_mails(request):
    message = "";
    for presenter in Presenter.objects.order_by('name'):
        if presenter.available:
            message += "\"" + presenter.name + "\" <" + presenter.email + ">, "
    response = HttpResponse(message, mimetype='text/plain')
    response['Filename'] = 'mails.txt'
    response['Content-Disposition'] = 'attachment; filename=mails.txt'
    return response
    
def send_announce(request):
    from mailMessages import getAnnounceMessage, getAnnounceSubject
    from mailHelper import mailWai
    if request.method == 'POST': # If the form has been submitted...
        form = SendAnnounceForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            mailWai(form.cleaned_data['subject'], form.cleaned_data['message'], settings.EMAIL_SENDER, settings.EMAIL_ANOUNCEMENT_RECIPIENTS)
            return HttpResponseRedirect("/page/schedule") # Redirect after POST
    else:
        meeting = get_object_or_404(Meeting, date=request.GET['id'])
        
        subject = getAnnounceSubject(meeting.date.strftime("%d %B %Y"), meeting.presenters(), meeting.location.name)
        presenters = []
        for pres in meeting.presentation_set.all():
            presenter = {
                'name': pres.presenter.name,
                'title': pres.title,
                'abstract': pres.abstract
            }
            presenters.append(presenter)
        message = getAnnounceMessage(meeting.date.strftime("%d %B %Y"), meeting.location.name, presenters, settings.EMAIL_FOOTER)
        default = {
            'subject' : subject,
            'message' : message
        }
        form = SendAnnounceForm(default, auto_id=False) # An unbound form

    return render_to_response('wai/send_announce.html', {'form': form}, context_instance=RequestContext(request))


def send_request(request):
    from mailMessages import getRequestMessage, getRequestSubject
    from mailHelper import mailWai
    if request.method == 'POST': # If the form has been submitted...
        form = SendRequestForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            meeting = get_object_or_404(Meeting, date=form.cleaned_data['identifier'])
            #cc = settings.EMAIL_REQUEST_ABSTRACT_CC
            to = settings.EMAIL_REQUEST_ABSTRACT_CC
            for pres in meeting.presentation_set.all():
                to.append(pres.presenter.email)
            mailWai(form.cleaned_data['subject'], form.cleaned_data['message'], settings.EMAIL_SENDER, to)
            return HttpResponseRedirect("/page/schedule") # Redirect after POST
    else:
        meeting = get_object_or_404(Meeting, date=request.GET['id'])
        subject = getRequestSubject()
        
        presenters = ""
        for pres in meeting.presentation_set.all():
            a = pres.presenter.name.split(' ')
            presenters += "%s, " % a[0]
        message = getRequestMessage(presenters, meeting.date.strftime("%d %B %Y"), settings.EMAIL_FOOTER)
        default = {
            'subject' : subject,
            'message' : message,
            'identifier' : request.GET['id']
        }
        form = SendRequestForm(default, auto_id=False) # An unbound form

    return render_to_response('wai/send_request.html', {'form': form}, context_instance=RequestContext(request))
    

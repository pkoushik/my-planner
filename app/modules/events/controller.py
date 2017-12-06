from __future__ import print_function
import json
import string
import re
import requests
import subprocess
import os
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from app.modules.auth.model import User
from app.modules.classes.model import Class
from app.modules.events.model import Event
from flask import Blueprint, render_template, flash, request, redirect, \
    url_for, jsonify
from flask_security import current_user, login_required
from bson import json_util
from dateutil.relativedelta import relativedelta
from datetime import timedelta, date
from datetime import datetime
# import argparse
#flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None



classes = Blueprint('classes', __name__)
APPLICATION_NAME = 'My Planner'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-myplanner.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = OAuth2WebServerFlow(client_id=os.environ.get('CLIENT_ID'),
                           client_secret=os.environ.get('CLIENT_SECRET'),
                           scope='https://www.googleapis.com/auth/calendar',
                           redirect_uri='http://localhost/classes')
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
#else: # Needed only for compatibility with Python 2.6
            #credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


events = Blueprint('events', __name__)

@events.route('/<class_id>/addEvent', methods=['POST'])
def add_event(class_id):
    print("tryna event rq")
    payload = request.get_json()
    c = Class.objects.get(id=class_id)
    user = current_user._get_current_object()
    name = payload[0]['name'] # name of the event
    date = payload[0]['date'] # day the event is due
    time = payload[0]['time'] # time due for the event
    typeOfEvent = payload[0]['typeOfEvent']

    print('time is ' + time)
    print('date is ' + date)

    # need to finna change date and time into DateTimeFields
    # datetime_of_time = datetime.strptime()

    total = date + ' ' + time
    print('total is ' + total)

    # total is 18 December, 2017 08:00PM (example)

    datetime_obj = datetime.strptime(total, '%d %B, %Y %I:%M%p')

    print('obj is ' + str(datetime_obj))


    current_event = Event(name=name, typeOfEvent=typeOfEvent, date_time=datetime_obj, time_str=datetime_obj.strftime('%b %d, %Y')).save()
    c.events.append(current_event)
    c.save()
    user.save()
    flash('success Added Assignment: {}'.format(current_event.name))

    createCalendarEvent(current_event)

    return json.dumps({'status': 'success'})


def createCalendarEvent(e):
    print("tryna create that calendar event")
    credentials = get_credentials()
    if not credentials:
        return
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    eventDate = e.date_time

    print(eventDate.strftime('%Y-%m-%d'))

    event ={
      'summary': e.name,
      'description': 'Created by MyPlanner',
      'start': {
        'dateTime': eventDate.strftime('%Y-%m-%dT%H:%M:%S-05:00'),
        'timeZone': 'America/Indiana/Indianapolis',
      },
      'end': {
        'dateTime': eventDate.strftime('%Y-%m-%dT%H:%M:%S-05:00'),
        'timeZone': 'America/Indiana/Indianapolis',
      },
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'minutes': 24 * 60},
          {'method': 'popup', 'minutes': 10},
        ],
      },
    }
    event = service.events().insert(calendarId='primary', body=event).execute()
    e.gcal_events.append(event['id'])
    e.save()
    return


@events.route('/<class_id>/deleteEvent', methods=['POST'])
def delete_event(class_id):
    print("im in the delete method yeee its litty squad fam")
    # print(class_id)

    payload = request.get_json()
    event_id = payload[0]['event_id']

    print(class_id) # got the id for the class
    print(event_id) # got the id for the event, this is what needs to be deleted

    currclass = Class.objects.get(id=class_id)

    currevent = Event.objects.get(id=event_id)
    delete_cal_events(currevent)
    currclass.events.remove(currevent) # finna delete the event from the class object
    # finna delete the event from the db
    currevent.delete()

    currclass.save()

    return json.dumps({'status': 'success'})

def delete_cal_events(c):
    print("delete calendar event")
    credentials = get_credentials()
    if not credentials:
        return
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    events = c.gcal_events
    print(len(events))
    for eventid in events:
        print(eventid)
        service.events().delete(calendarId='primary', eventId=eventid).execute()

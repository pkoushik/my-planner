from __future__ import print_function
import json
import string
import re
import requests
import subprocess
import datetime
import os
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from app.modules.auth.model import User
from app.modules.classes.model import Class
from app.modules.events.model import Event
from flask import Blueprint, render_template, flash, request, redirect, \
    url_for, jsonify
from flask_security import current_user, login_required
from bson import json_util
from dateutil.relativedelta import relativedelta
from datetime import timedelta, date


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None



classes = Blueprint('classes', __name__)

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


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
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


events = Blueprint('events', __name__)

@events.route('/<class_id>/addEvent', methods=['POST'])
def add_event(class_id):
    print("tryna event rq")
    payload = request.get_json()
    c = Class.objects.get(id=class_id)
    user = current_user._get_current_object()
    name = payload[0]['name']
    print(name)

    current_event = Event(name=name, typeOfEvent="").save()
    c.events.append(current_event)
    c.save()
    user.save()
    flash('success Added Assignment: {}'.format(current_event.name))

    createCalendarEvent(current_event)

    return json.dumps({'status': 'success'})

def createCalendarEvent(e):
    print("tryna create that calendar event")
    credentials = get_credentials()

    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    eventDate = e.time

    print(eventDate.strftime('%Y-%m-%d'))

    event ={
      'summary': e.name,
      'description': 'Class',
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
    return redirect(request.args.get('next') or url_for('classes.home'))

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
#from app.modules.events.model import Event
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

from datetime import datetime
# from app.modules.events.controller import delete_event


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

def filter_form(form):
    """ Router for CRUD Forms that were Recieved on the Group Dashboard """
    print("trying to filter")
    if form['submit'] == 'create':
        return add_class(form)
    # elif form['submit'] == 'update':
    #     return update_group(form)
    # elif form['submit'] == 'delete':
    #     return delete_group(form)

    flash('error Could not Fulfill Request. Please Try Again.')
    return redirect(url_for('classes.home'))


@classes.route('/', methods=['GET', 'POST'])
@login_required
def home():
    """ Displays All of the Current Users Classes"""
    if request.method == 'POST':
        print("in post")
        return redirect(url_for('classes.home'))
    print("in get")
    user = current_user._get_current_object()
    return render_template('classes/classes.html', classes=user.classes, user=user)

# @classes.route('/<class_id>', methods=['GET'])
# @login_required
# def add_class(form=None):
#     if form is None:
#         flash('Invalid request to add a class')
#
#     add_class_form = CreateClassForm(form) # form to add a class
#
#     if not add_class_form.validate():
#         print(add_class_form.name)
#         print(add_class_form.professor)
#         print(add_class_form.days)
#         flash('Invalid information was provided in creating a class. Please try again.')
#         return redirect(request.args.get('next') or url_for('classes.home'))
#
#
#     # form is valid
#     try:
#         user = current_user._get_current_object()
#
#         # class that is created from the form
#         current_class = Class(owner=user, name=add_class_form.name.data, professor = add_class_form.professor.data, days = [add_class_form.days.data]).save()

@classes.route('/<class_id>', methods=['GET'])
@login_required
def getEvents(class_id):
    print("yooo im cool man guy")
    c = Class.objects.with_id(class_id)
    user = current_user._get_current_object()
    return render_template('events/events.html', c=c, user=user)


@classes.route('/addClass', methods=['POST'])
def add_class():
    payload = request.get_json()    # try:
    user = current_user._get_current_object()
    name = payload[0]['name']
    print(name)
    prof = payload[0]['professor']
    print(prof)
    days = payload[0]['days']
    print(days)
    start_date = payload[0]['start_date']
    print(start_date)
    end_date = payload[0]['end_date']
    print(end_date)
    start_time = payload[0]['start_time']
    print(start_time)
    end_time = payload[0]['end_time']
    print(end_time)

    datetime_start_date = datetime.strptime(start_date, '%d %B, %Y')
    datetime_end_date = datetime.strptime(end_date, '%d %B, %Y')

    datetime_start_time = datetime.strptime(start_time, '%I:%M%p')
    datetime_end_time = datetime.strptime(end_time, '%I:%M%p')


    current_class = Class(owner=user, name=name, professor=prof)
    current_class.days = days
    current_class.start_date = datetime_start_date
    current_class.end_date = datetime_end_date
    current_class.start_time = datetime_start_time
    current_class.end_time = datetime_end_time
    current_class.save()

    user.classes.append(current_class)
    user.save()

    createCalendarEvents(current_class)
    flash('success Added Class: {}'.format(current_class.name))
    return redirect(request.args.get('next') or url_for('classes.home'))

@classes.route('/<class_id>/deleteClass', methods=['POST'])
def delete_class(class_id):
    print("finna delete a class")
    print(class_id)
    currclass = Class.objects.get(id=class_id)
    delete_cal_events(currclass)
    # need to finna delete every event from currclass
    for event in currclass.events:
        event.delete()
        currclass.events.remove(event)
    # all the events should be deleted from the class
    curruser = current_user._get_current_object()
    curruser.classes.remove(currclass) # removing the class from the users database
    curruser.save()
    currclass.delete()
    return json.dumps({'status': 'success'})


# sourced from https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def createCalendarEvents(c):
    print("tryna create that calendar event")
    credentials = get_credentials()

    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    startDate = c.start_date
    endDate = c.end_date
    startTime = c.start_time
    endTime = c.end_time

    for date in daterange(startDate,endDate):
        #print(date.weekday())
        if str(date.weekday()) in c.days:
            ed = date
            sd = date

            ed = ed+ relativedelta(hours=endTime.hour)
            ed = ed + relativedelta(minutes=endTime.minute)

            sd = sd+ relativedelta(hours=startTime.hour)
            sd = sd + relativedelta(minutes=startTime.minute)

            event ={
              'summary': c.name,
              'description': 'Created by MyPlanner', # c.professor'',  #"Professor: "+str(c.professor),
              'start': {
                'dateTime': sd.strftime('%Y-%m-%dT%H:%M:%S-05:00'),
                'timeZone': 'America/Indiana/Indianapolis',
              },
              'end': {
                'dateTime': ed.strftime('%Y-%m-%dT%H:%M:%S-05:00'),
                'timeZone': 'America/Indiana/Indianapolis',
              },
              'reminders': {
                'useDefault': False,
                'overrides': [
                  {'method': 'email', 'minutes': 24 * 60},
                  {'method': 'popup', 'minutes': 30},
                ],
              },
            }
            event = service.events().insert(calendarId='primary', body=event).execute()
            c.gcal_events.append(event['id'])
            c.save()
    return
    # return json.dumps({'status': 'success'})

def delete_cal_events(c):
    print("delete calendar event")
    credentials = get_credentials()

    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    events = c.gcal_events
    print(len(events))
    for eventid in events:
        print(eventid)
        service.events().delete(calendarId='primary', eventId=eventid).execute()

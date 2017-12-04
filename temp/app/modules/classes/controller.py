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
    payload = request.get_json()
    try:
        user = current_user._get_current_object()
        name = payload[0]['name']
        print(name)
        prof = payload[0]['professor']
        print(prof)

        current_class = Class(owner=user, name=name, professor=prof, days = []).save()
        user.classes.append(current_class)
        user.save()
        flash('success Added Class: {}'.format(current_class.name))

        createCalendarEvents(current_class)

    except Exception as e:
        flash('error An Error has occured, Please Try Again. {}'.format(e))

    return redirect(request.args.get('next') or url_for('classes.home'))


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
    endDate = c.end_date+ datetime.timedelta(days=+100)

    print(endDate.strftime('%Y-%m-%d'))

    c.days = [0,2,4]
    for date in daterange(startDate,endDate):
        print(date.weekday())
        if date.weekday() in c.days:
            print("yay!!!")
            event ={
              'summary': 'Created by MyPlanner',
              'description': 'Class',
              'start': {
                'dateTime': date.strftime('%Y-%m-%dT%H:%M:%S-05:00'),
                'timeZone': 'America/Indiana/Indianapolis',
              },
              'end': {
                'dateTime': (date+ datetime.timedelta(hours=+1)).strftime('%Y-%m-%dT%H:%M:%S-05:00'),
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

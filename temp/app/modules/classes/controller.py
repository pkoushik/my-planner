import json
import string
import re
import requests
import subprocess
import datetime
from app.modules.auth.model import User
from app.modules.classes.model import Class
from app.modules.events.model import Event
from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify
from flask_security import current_user, login_required
from bson import json_util1


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
                                   'calendar-python-quickstart.json')

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


@classes.route('/', methods=['GET', 'POST'])
@login_required
def home():
    """ Displays All of the Current Users Classes"""
    if request.method == 'POST':
        return filter_form(request.form)
    user = current_user._get_current_object()
    return render_template('classes/dashboard.html', classes=user.classes, form=form)

@classes.route('/addClass', methods=['POST'])
@login_required
def add_class(form=None):
    if form is None:
        flash('Invalid request to add a class')

    add_class_form = AddClassForm() # form to add a class

    if not form.validate():
    	flash('Invalid information was provided in creating a class. Please try again.')
    	return redirect(request.args.get('next') or url_for('classes.home'))


    # form is valid
    try:
    	user = current_user._get_current_object()

    	# class that is created from the form
    	current_class = Class(owner=user,name=add_class_form.name.data, person = add_class_form.person.data, start_time = add_class_form.start_time.data,
    	 end_time = add_class_form.end_time.data, days = add_class_form.days.data, start_date = add_class_form.start_date.data, end_date = add_class_form.end_date.data)

    	user.classes.append(current_class)

        createCalendarEvents(current_class)

    except Exception as e:
    	flash('error An Error has occurred, Please Try Again. {}'.format(e))

# sourced from https://tudorbarbu.ninja/iterate-thru-dates-in-python/
def daterange( start_date, end_date ):
    if start_date &lt;= end_date:
        for n in range( ( end_date - start_date ).days + 1 ):
            yield start_date + datetime.timedelta( n )
    else:
        for n in range( ( start_date - end_date ).days + 1 ):
            yield start_date - datetime.timedelta( n )
def createCalendarEvents(Class c):
    startDate = user.start_date
    endDate = user.end_date
    event ={
      'summary': 'Google I/O 2015',
      'location': '800 Howard St., San Francisco, CA 94103',
      'description': 'A chance to hear more about Google\'s developer products.',
      'start': {
        'dateTime': '2017-12-28T09:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
      },
      'end': {
        'dateTime': '2017-12-28T17:00:00-07:00',
        'timeZone': 'America/Los_Angeles',
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


    #for date in daterange(start,end):
    #    if date.datetime.today() in c.days:
    #        event = {
    #
    #        }

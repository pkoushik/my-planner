import json
import string
import re
import requests
import subprocess
from app.modules.auth.model import User
from app.modules.classes.model import Class
#from app.modules.events.model import Event
from flask import Blueprint, render_template, flash, request, redirect, \
    url_for, jsonify
from flask_security import current_user, login_required
from bson import json_util
from datetime import datetime
# from app.modules.events.controller import delete_event


classes = Blueprint('classes', __name__)

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
    # try:
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
    current_class.end_date = datetime_end_time
    current_class.start_time = datetime_start_time
    current_class.end_time = datetime_end_time
    current_class.save()

    user.classes.append(current_class)
    user.save()
    flash('success Added Class: {}'.format(current_class.name))

    #except Exception as e:
    #    flash('error An Error has occured, Please Try Again. {}'.format(e))

    return json.dumps({'status': 'success'})

@classes.route('/<class_id>/deleteClass', methods=['POST'])
def delete_class(class_id):
    print("finna delete a class")

    print(class_id)

    currclass = Class.objects.get(id=class_id)

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

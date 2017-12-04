import string
import json
from app.modules.auth.model import User
from app.modules.events.model import Event
from app.modules.classes.model import Class
from flask import Blueprint, request, render_template, flash, redirect, \
    url_for, jsonify
from flask_security import login_required, current_user
from datetime import datetime


events = Blueprint('events', __name__)

@events.route('/<class_id>/addEvent', methods=['POST'])
def add_event(class_id):
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
    

    current_event = Event(name=name, typeOfEvent=typeOfEvent, date_time=datetime_obj).save()
    c.events.append(current_event)
    c.save()
    user.save()
    flash('success Added Assignment: {}'.format(current_event.name))

    return json.dumps({'status': 'success'})


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

    currclass.events.remove(currevent) # finna delete the event from the class object

    

    # finna delete the event from the db

    currevent.delete()

    currclass.save()





    return json.dumps({'status': 'success'})

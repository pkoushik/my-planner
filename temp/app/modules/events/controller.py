import string
import json
from app.modules.auth.model import User
from app.modules.events.model import Event
from app.modules.classes.model import Class
from flask import Blueprint, request, render_template, flash, redirect, \
    url_for, jsonify
from flask_security import login_required, current_user


events = Blueprint('events', __name__)

@events.route('/<class_id>/addEvent', methods=['POST'])
def add_event(class_id):
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

    return json.dumps({'status': 'success'})


@events.route('/<class_id>/deleteEvent', methods=['POST'])
def delete_event(class_id):
    payload = request.get_json()
    currclass = Class.objects.get(id=class_id)
    event_id = payload[0]['event_id']

    # print('the events of this class are ')
    # print(str(currclass.events))

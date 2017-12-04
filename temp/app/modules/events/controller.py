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

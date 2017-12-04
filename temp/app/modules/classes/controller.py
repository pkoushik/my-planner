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

    current_class = Class(owner=user, name=name, professor=prof, days = "").save()
    user.classes.append(current_class)
    user.save()
    flash('success Added Class: {}'.format(current_class.name))

    #except Exception as e:
    #    flash('error An Error has occured, Please Try Again. {}'.format(e))

    return json.dumps({'status': 'success'})

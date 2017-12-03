import json
import string
import re
import requests
import subprocess
from app.modules.auth.model import User
from app.modules.classes.model import Class
#from app.modules.events.model import Event
from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify
from flask_security import current_user, login_required
from bson import json_util

classes = Blueprint('classes', __name__)

@classes.route('/', methods=['GET', 'POST'])
@login_required
def home():
    """ Displays All of the Current Users Classes"""
    if request.method == 'POST':
        return filter_form(request.form)
    user = current_user._get_current_object()
    return render_template('classes/dashboard.html', classes=user.classes, user=user)

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

    except Exception as e:
    	flash('error An Error has occurred, Please Try Again. {}'.format(e))

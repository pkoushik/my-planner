import json
import string
import re
import requests
import subprocess
from app.modules.auth.model import User
from app.modules.classes.model import Class, CreateClassForm
#from app.modules.events.model import Event
from flask import Blueprint, render_template, flash, request, redirect, \
    url_for, jsonify
from flask_security import current_user, login_required
from bson import json_util

classes = Blueprint('classes', __name__)

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
        return filter_form(request.form)
    user = current_user._get_current_object()
    form = CreateClassForm()
    return render_template('classes/classes.html', classes=user.classes, user=user, form=form)

@classes.route('/addClass', methods=['POST'])
@login_required
def add_class(form=None):
    if form is None:
        flash('Invalid request to add a class')

    add_class_form = CreateClassForm(form) # form to add a class

    if not add_class_form.validate():
        print(add_class_form.name)
        print(add_class_form.professor)
        print(add_class_form.days)
        flash('Invalid information was provided in creating a class. Please try again.')
        return redirect(request.args.get('next') or url_for('classes.home'))


    # form is valid
    try:
        user = current_user._get_current_object()

        # class that is created from the form
        current_class = Class(owner=user, name=add_class_form.name.data, professor = add_class_form.professor.data, days = add_class_form.days.data).save()

        user.classes.append(current_class)
        user.save()
        valid_emails = ["idk"]

        flash('success Added Class: {}'.format(current_class.name))

    except Exception as e:
        flash('error An Error has occured, Please Try Again. {}'.format(e))

    return redirect(request.args.get('next') or url_for('classes.home'))

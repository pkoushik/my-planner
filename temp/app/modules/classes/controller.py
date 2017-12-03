import json
import string
import re
import requests
import subprocess
from app.modules.auth.model import User
from app.modules.classes.model import Class
from app.modules.events.model import Event
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
    return render_template('classes/dashboard.html', classes=user.classes, form=form)

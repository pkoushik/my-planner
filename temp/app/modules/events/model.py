from app import db

from app.modules.auth.model import User
from app.modules.classes.model import Class

from wtforms import Form, validators, SelectField
from wtforms import StringField


class Events(db.Document):
    """ Definition for a Role Document needed by Flask Security """
    name = db.StringField(max_length=80)
    typeOfEvent = db.StringField(max_length=80)
    time = db.DateTimeField()
    meta = {'strict': False}

class EventCreateForm(Form):
	# validators.Length checks for the length of a string
	# .dataRequired is checking that something was inputted?
	name = StringField('Name of Assignment', [validators.Length(min=0, max=100),
												validators.DataRequired()])
	time = db.DateTimeField()
	


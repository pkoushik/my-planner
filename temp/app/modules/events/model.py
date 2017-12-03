from app import db
from datetime import datetime as dt

from app.modules.auth.model import User
# from app.modules.classes.model import Class

from wtforms import Form, validators, SelectField, StringField, RadioField


class Event(db.Document):
    """ Definition for a Role Document needed by Flask Security """
    name = db.StringField(max_length=80)
    typeOfEvent = db.StringField(max_length=80)
    time = db.DateTimeField()
    #time_str = db.StringField(time.strftime('%m-%d-%Y'))
    # event_class = db.ReferenceField(Class, required=True)
    meta = {'strict': False}

class CreateEventForm(Form):
	# validators.Length checks for the length of a string
	# .dataRequired is checking that something was inputted?
	name = StringField('Name of Assignment', [validators.Length(min=0, max=100),
												validators.DataRequired()])
	time = db.DateTimeField()
	typeOfEvent = RadioField('Type of Assignment',
	choices=[('homework', 'Homework'), ('test', 'Test'), ('quiz', 'Quiz'), ('presentation', 'Presentation'), ('lab', 'Lab'),
					('final', 'Final'), ('midterm', 'Midterm'), ('project', 'Project')])
	# need to set the class that the event belongs to

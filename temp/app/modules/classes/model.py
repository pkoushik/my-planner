from app import db
from datetime import datetime as dt

from app.modules.auth.model import User

from wtforms import Form, validators, StringField, RadioField, \
    SelectMultipleField, DateTimeField

class Class(db.Document):
    owner = db.ReferenceField(User, required=True)
    name = db.StringField(required=True, min_length=3, max_length=50)
    professor = db.ReferenceField(User, required=True)
    #events = db.ListField(db.ReferenceField(Events))
    start_time = db.DateTimeField(default=dt.now())
    end_time = db.DateTimeField(default=dt.now())
    days = db.ListField(db.StringField(default="",required=True))
    start_date = db.DateField(default=dt.now())
    end_date = db.DateField(default=dt.now())
    meta = {'strict': False}

class CreateClassForm(Form):
    name = StringField('Class Name', [validators.Length(min=3, max=100),
                                        validators.DataRequired()])
    professor = StringField('Professor Name', [validators.DataRequired()])
    days = RadioField('Days of the Week', choices=[
        ('sunday', 'Sunday'), ('monday', 'Monday'), ('tuesday', "Tuesday"),
        ('wednesday', 'Wednesday'), ('thursday', 'Thursday'),
        ('friday', "Friday")])
    # start_date = DateTimeField('Start Date', format='%Y-%m-%d %H:%M:%S')
    # end_date = DateTimeField('End Date', format='%Y-%m-%d %H:%M:%S')
    # class_start_time = DateTimeField('Start Time', format='%Y-%m-%d %H:%M:%S')
    # class_end_time = DateTimeField('End Time', format='%Y-%m-%d %H:%M:%S')

from app import db
from datetime import datetime as dt

from app.modules.auth.model import User
# from app.modules.classes.model import Class

from wtforms import Form, validators, SelectField, StringField, RadioField


class Event(db.Document):
    """ Definition for a Role Document needed by Flask Security """
    #owner = db.ReferenceField(User, required=True)
    name = db.StringField(max_length=80)
    typeOfEvent = db.StringField(max_length=80)
    time = db.DateTimeField(default=dt.now())
    #time_str = db.StringField(time.strftime('%m-%d-%Y'))
    # event_class = db.ReferenceField(Class, required=True)
    meta = {'strict': False}

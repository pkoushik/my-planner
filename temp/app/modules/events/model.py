from app import db

from app.modules.auth.model import User
from app.modules.classes.model import Class

from wtforms import Form, validators
from wtforms import StringField


class Events(db.Document):
    """ Definition for a Role Document needed by Flask Security """
    name = db.StringField(max_length=80)
    typeOfEvent = db.StringField(max_length=80)
    time = db.DateTimeField()
    meta = {'strict': False}

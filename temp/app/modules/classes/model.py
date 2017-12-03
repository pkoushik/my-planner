from app import db
from datetime import datetime as dt

from app.modules.auth.model import User

from wtforms import Form, validators, StringField, RadioField

class Class(db.Document):
    name = db.StringField(required=True, min_length=3, max_length=50)
    person = db.ReferenceField(User, required=True)
    events = db.ListField(db.ReferenceField(Events))
    time = db.DateTimeField(default=dt.now())
    meta = {'strict': False}

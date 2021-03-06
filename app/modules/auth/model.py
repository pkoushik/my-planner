from app import app, db

from flask_security import Security, MongoEngineUserDatastore, \
    UserMixin , RoleMixin
from wtforms import Form, StringField, PasswordField, validators

class Role(db.Document, RoleMixin):
    name = db.StringField(max_length=80, unique=True)
    description = db.StringField(max_length=255)


class User(db.Document, UserMixin):
    meta = {'strict': False}

    # identity fields
    email = db.EmailField(required=True, unique=True,
                          min_length=3, max_length=35)
    name = db.StringField(required=True, min_length=4, max_length=20)
    password = db.StringField(required=True, min_length=5, max_length=1000)

    # myplanner fields
    classes = db.ListField(db.ReferenceField('Class'), default=[])

    # authentication fields
    activation_hash = db.StringField()
    password_reset_hash = db.StringField()

    # security fields
    active = db.BooleanField(default=False)
    roles = db.ListField(db.ReferenceField(Role), default=[])

    def is_active(self):
        """ Determines if a User is currently active """
        return self['active']

    def is_anonymous(self):
        """ Determines if a User is anonymous; this will always return false
        becuase anonymous users are not currently supported """
        return False

    def get_id(self):
        """ Fetches the unicode id for the User """
        return str(User.objects.get(email=self['email']).id)

class SignupForm(Form):
    email = StringField('Email', [validators.DataRequired(),
                                  validators.Length(min=6, max=35)])
    name = StringField('Name', [validators.DataRequired(),
                                validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired(),
                                          validators.Length(min=5, max=35)])


class LoginForm(Form):
    email = StringField('Email', [validators.DataRequired(),
                                  validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.DataRequired(),
                                          validators.Length(min=5, max=35)])


# Flask-Security Setup
user_datastore = MongoEngineUserDatastore(db, User, Role)
security = Security(app, user_datastore)

# Authentication Setup
# mail = SendGrid(app)

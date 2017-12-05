from flask import Flask
from flask_mongoengine import MongoEngine

# Initialize the app
myapp = Flask(__name__)
myapp.config.from_object('config')

# Define the database
db = MongoEngine(myapp)


@myapp.route('/')
def index():
    return '<h1> MyPlanner Home </h1>'

# Import Blueprint modules
from app.modules.auth.controller import auth
from app.modules.classes.controller import classes
from app.modules.events.controller import events

# Register Blueprints
myapp.register_blueprint(auth, url_prefix='/auth')
myapp.register_blueprint(classes, url_prefix='/classes')
myapp.register_blueprint(events, url_prefix='/events')

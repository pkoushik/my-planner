from flask import Flask, redirect, url_for
from flask_mongoengine import MongoEngine

# Initialize the app
app = Flask(__name__)
app.config.from_object('config')

# Define the database
db = MongoEngine(app)

@app.route('/', strict_slashes=False)
def index():
    return redirect(url_for('auth.login'))

# Import Blueprint modules
from app.modules.auth.controller import auth
from app.modules.classes.controller import classes
from app.modules.events.controller import events

# Register Blueprints
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(classes, url_prefix='/classes')
app.register_blueprint(events, url_prefix='/events')
from flask import Flask
from flask_mongoengine import MongoEngine

# Initialize the app
app = Flask(__name__)
app.config.from_object('config')

# Define the database
db = MongoEngine(app)


@app.route('/')
def index():
    return '<h1> myplanner Home </h1>'


# Import Blueprint modules
from app.modules.auth.controller import auth

# Register Blueprints
app.register_blueprint(auth, url_prefix='/auth')

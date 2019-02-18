import os, secrets
from flask import Flask
from flask_socketio import SocketIO
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from pymongo import MongoClient

#Set up the flask-app
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(60)
socketio = SocketIO(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

#Set up MongoDB
client = MongoClient('mongo',27017)
db = client.webDB
user = db.Users

#Bcrypt for storing passwords
bcrypt = Bcrypt(app)

#Construct dependent things
from website import routes

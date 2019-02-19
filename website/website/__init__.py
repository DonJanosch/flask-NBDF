import os, secrets
from flask import Flask
from flask_socketio import SocketIO
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

#Set up the flask-app
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(60)

#Mixins and extensions
socketio = SocketIO(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

#Set up the Database
DATABASE_TYPE = os.environ['DATABASE_TYPE']
DATABASE_NAME = os.environ['DATABASE_NAME']
PASSWORD = os.environ['DATABASE_ROOT_PASSWORD']
USER = os.environ['DATABASE_ROOT_USER']
HOSTNAME = 'db' # Used with docker-compose, is the name of the db-service
app.config['SQLALCHEMY_DATABASE_URI'] = f'{DATABASE_TYPE}://{USER}:{PASSWORD}@{HOSTNAME}/{DATABASE_NAME}'
db = SQLAlchemy(app)

#Bcrypt for storing passwords
bcrypt = Bcrypt(app)

#Construct dependent things
from website import routes

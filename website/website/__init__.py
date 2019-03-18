import os, secrets
from flask import Flask, redirect, url_for
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_socketio import SocketIO, send
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from apscheduler.schedulers.blocking import BlockingScheduler

#Set up the flask-app
app = Flask(__name__)
app.config.from_pyfile('mailserver.cfg')
app.config['SECRET_KEY'] = secrets.token_hex(60)
mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

#Set up the Database
DATABASE_TYPE = os.environ['DATABASE_TYPE']
DATABASE_NAME = os.environ['DATABASE_NAME']
PASSWORD = os.environ['DATABASE_ROOT_PASSWORD']
USER = os.environ['DATABASE_ROOT_USER']
HOSTNAME = 'db' # Used with docker-compose, is the name of the db-service
app.config['SQLALCHEMY_DATABASE_URI'] = f'{DATABASE_TYPE}://{USER}:{PASSWORD}@{HOSTNAME}/{DATABASE_NAME}'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

#Construct the email-scheduler-process
email_scheduler = BlockingScheduler()
email_scheduler.add_jobstore('sqlalchemy', url=app.config['SQLALCHEMY_DATABASE_URI'])

#Construct dependent things
from website import routes
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
db.create_all()

#Construct SocketIOsocketio = SocketIO(app)
socketio = SocketIO(app)
from website.socketio import *

print('Loaded website')

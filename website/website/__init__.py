import os, secrets
from flask import Flask, redirect, url_for
from flask_socketio import SocketIO
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

#Set up the flask-app
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(60)
socketio = SocketIO(app)

#Set up the Database
DATABASE_TYPE = os.environ['DATABASE_TYPE']
DATABASE_NAME = os.environ['DATABASE_NAME']
PASSWORD = os.environ['DATABASE_ROOT_PASSWORD']
USER = os.environ['DATABASE_ROOT_USER']
HOSTNAME = 'db' # Used with docker-compose, is the name of the db-service
app.config['SQLALCHEMY_DATABASE_URI'] = f'{DATABASE_TYPE}://{USER}:{PASSWORD}@{HOSTNAME}/{DATABASE_NAME}'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

#Construct dependent things
from website import routes
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
db.create_all()

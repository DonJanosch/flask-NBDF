import enum

from datetime import datetime
from flask import redirect, url_for
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

from website import app, db

class PilotType(enum.Enum):
    Gleitschirm = 'Gleitschirm'
    Drache = 'Drache'
    GleitschirmDrache = 'GleitschirmDrache'
    Fußgänger = 'Fußgänger'

UserType = (
    'WinchOperatorEWF',
    'WinchOperatorGSDR',
    'WinchOperatorDR',
    'WinchOperatorGS',
    'Helper',
    'Member',
    'Guest',
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30), nullable=False)
    lastname = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    paraglider = db.Column(db.String(100),nullable=True)
    is_member = db.Column(db.Boolean, default=False)
    is_windenfahrer = db.Column(db.Boolean, default=False)
    is_ewf = db.Column(db.Boolean, default=False)
    is_validated = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    confirmation_link = db.Column(db.String(500), nullable=False)

    def __repr__(self):
        return f'User({self.firstname}, {self.lastname}, {self.email}, {self.image_file})'

class Post(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'Post({self.title}, {self.date_posted})'

#Configure the Admin-Area
class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        # TODO: User-Classes deffinieren, damit nur Admins die Seite sehen können.
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login'))

admin = Admin(app, index_view=MyAdminIndexView())
admin.add_view(MyModelView(User, db.session))

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

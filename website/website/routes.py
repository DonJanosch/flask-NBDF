from flask import flash, redirect, url_for, request, render_template
from datetime import datetime
from flask_login import login_user

from website import app, bcrypt, db, user, login_manager
from website.forms import RegistrationForm, LoginForm
from website.tools.calendar import make_example_set_of_assigned_fly_days

posts = [
    {
        'author':'John Doe',
        'title':'Blog Post 1',
        'content':'First post content',
        'date_posted': '01.01.2019',
    },
    {
        'author':'Jan Macenka',
        'title':'Wirklich wichtig',
        'content':'Den hund noch füttern',
        'date_posted': '01.01.2019',
    },
]

@login_manager.user_loader
def load_user(user_id):
    return user.find_one({'_id':user_id})

def exists(query):
    if len([x for x in query]) > 0:
        return True
    return False

@app.route('/examples')
@app.route('/example')
def example_fly_days():
    list_of_weekends, _ = make_example_set_of_assigned_fly_days()
    context = {
        '_ul_list':list_of_weekends,
        'title':'Beispielliste'
    }
    return render_template('example_fly_days.html',**context)

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html',posts=posts, title='test')

@app.route('/kontakt')
def about():
    return render_template('index.html')

@app.route('/anmelden', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = {
            'firstname':form.firstname.data,
            'lastname':form.lastname.data,
            'email':form.email.data,
            'password':hashed_password
        }
        user.insert_one(new_user)
        flash(f'Willkommen {form.firstname.data}, du bist jetzt registriert!','success')
        return redirect(url_for('login'))
    context = {
        'form':form,
        'title':'Registrieren',
    }
    return render_template('register.html',**context)

@app.route('/login', methods=['POST','GET'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if bcrypt.check_password_hash(user.find_one({'email':form.email.data})['password'],form.password.data):
            logged_in_user = user.find_one({'email':form.email.data})
            flash(f'Willkommen {logged_in_user["firstname"]}.','success')
            login_user(logged_in_user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Das hat nicht geklappt.Email oder Password sind nicht korrekt.', 'danger')
    context = {
        'form':form,
        'title':'Einloggen',
    }
    return render_template('login.html',**context)

@app.route('/users')
def show_users():
    all_users = [user for user in user.find()]
    context = {
        'users':all_users
    }
    return render_template('users.html',**context)

@app.route('/users/undo')
def undo_users():
    user.drop()
    flash(f'All Users have been droped.')
    return render_template('index.html')

@app.route('/user/<lastname>')
def get_user(lastname):
    context = {
        'users':user.find({'lastname':lastname})
    }
    if exists(user.find({'lastname':lastname})):
        return render_template('users.html',**context)
    else:
        return 'nichts gefunden'

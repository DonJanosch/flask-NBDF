import random
from flask import flash, redirect, url_for, request, render_template
from datetime import datetime
from flask_login import login_user, logout_user, login_required, current_user

from website import app, bcrypt, db, login_manager
from website.models import User
from website.forms import RegistrationForm, LoginForm
from website.tools.windenfahrer import make_example_set_of_assigned_fly_days
from website.tools.calendar import calendar_columwise

possible_weather = ['clouds']#,'fog','thunderstorm','sunshine']

@app.route('/example')
@login_required
def example():
    list_of_weekends, _ = make_example_set_of_assigned_fly_days()
    weather = random.choice(possible_weather)
    context = {
        '_ul_list':list_of_weekends,
        'title':'Beispielliste',
        'weather':weather,
    }
    return render_template('example.html',**context)

@app.route('/')
def home():
    weather = random.choice(possible_weather)
    context = {
        'title':'NBDF Homepage',
        'weather': weather,
    }
    return render_template('index.html',**context)

@app.route('/kontakt')
def about():
    return render_template('index.html')

@app.route('/anmelden', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user_data = {
            'firstname':form.firstname.data,
            'lastname':form.lastname.data,
            'email':form.email.data,
            'password':hashed_password
        }
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()
        flash(f'Willkommen {form.firstname.data}, du bist jetzt registriert!','success')
        return redirect(url_for('login'))
    context = {
        'form':form,
        'title':'Registrieren',
    }
    return render_template('register.html',**context)

@app.route('/login', methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if request.method == 'POST':
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next','home')
            return redirect(url_for(next_page.strip('/')))
        flash('Das hat nicht geklappt. Email oder Password sind nicht korrekt.', 'danger')
    context = {
        'form':form,
        'title':'Einloggen',
    }
    return render_template('login.html',**context)

@app.route('/logout')
@login_required
def logout():
    flash(f'Du bist ausgeloggt. Bis bald, {current_user.firstname}.','info')
    logout_user()
    return redirect(url_for('home'))

@app.route('/calendar')
def calendar():
    context = {
        'calendar_columwise':calendar_columwise
    }
    return render_template('calendar.html',**context)

@app.route('/account')
@login_required
def account():
    context = {
        'title':f'{current_user.firstname}\'s Account',
    }
    return render_template('account.html')

import random
from flask import flash, redirect, url_for, request, render_template
from datetime import datetime
from flask_login import login_user, logout_user, login_required, current_user

from website import app, db, bcrypt
from website.models import admin, login_manager, User
from website.forms import RegistrationForm, LoginForm, UpdateAccountForm
from website.tools.windenfahrer import make_example_set_of_assigned_fly_days
from website.tools.calendar import calendar_columwise

possible_weather = ['clouds']#,'fog','thunderstorm','sunshine']

context = {
    'copyright_year':datetime.now().year,
}

@app.route('/example')
@login_required
def example():
    list_of_weekends, _ = make_example_set_of_assigned_fly_days()
    context['_ul_list'] = list_of_weekends
    context['title'] = 'Beispielliste'
    context['weather'] = random.choice(possible_weather)
    return render_template('example.html',**context)

@app.route('/')
def home():
    context['title'] = 'NBDF Homepage'
    context['weather'] = random.choice(possible_weather)
    return render_template('home.html',**context)

@app.route('/kontakt')
def about():
    return render_template('about.html',**context)

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
        #context['user_email'] = form.email.data
        return redirect(url_for('login',**context))
    context['form'] = form
    context['title'] = 'Registrieren'
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
    context['form'] = form
    context['title'] = 'Einloggen'
    return render_template('login.html',**context)

@app.route('/logout')
@login_required
def logout():
    flash(f'Du bist ausgeloggt. Bis bald, {current_user.firstname}.','info')
    logout_user()
    return redirect(url_for('home'))

@app.route('/calendar')
def calendar():
    context['calendar_columwise'] = calendar_columwise
    return render_template('calendar.html',**context)

@app.route('/account')
@login_required
def account():
    # context['form'] = UpdateAccountForm()
    context['title'] = f'{current_user.firstname}\'s Account'
    context['image_file'] = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    return render_template('account.html',**context)

import random, os
from flask import flash, redirect, url_for, request, render_template, Markup
from datetime import datetime
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature

from website import app, db, bcrypt, mail, serializer
from website.models import admin, login_manager, User
from website.forms import RegistrationForm, LoginForm, UpdateAccountForm, RegisterNotificationForm
from website.tools.windenfahrer import make_example_set_of_assigned_fly_days
from website.tools.calendar import calendar_columwise
from website.tools.utils import load_script_from_filename
from website.notifications import resolve_datetime, schedule_new_email

possible_weather = ['clouds']#,'fog','thunderstorm','sunshine']
server_IP = os.environ['BACKEND_IP'].strip('"')

# Setting some global avaliable context wich is not dependent on the view.
def global_context():
    context = dict()
    context['copyright_year'] = datetime.now().year
    context['header_scripts'] = []
    context['body_scripts'] = 'jquery-3.3.1.min.js popper.min.js bootstrap.bundle.min.js'.split(' ')
    return context

@app.route('/register_notification', methods=['POST', 'GET'])
@login_required
def register_notification():
    context = global_context()
    form = RegisterNotificationForm()
    if form.validate_on_submit():
        topic = form.topic.data
        message = form.message.data
        notification_time = resolve_datetime(form.notification_time)
        schedule_new_email(topic, message, notification_time)
        flash(f'Registered Email for {current_user.email} to be sent at {notification_time}','success')
        return redirect(url_for('register_notification',**context))
    elif request.method == 'POST':
        flash(f'Something went wrong','warning')
        return redirect(url_for('register_notification',**context))
    context['form'] = form
    context['title'] = 'Register Notification'
    return render_template('register_notification.html',**context)

@app.route('/example')
@login_required
def example():
    context = global_context()
    list_of_weekends, _ = make_example_set_of_assigned_fly_days()
    context['_ul_list'] = list_of_weekends
    context['title'] = 'Beispielliste'
    context['weather'] = random.choice(possible_weather)
    return render_template('example.html',**context)

@app.route('/')
def home():
    context = global_context()
    context['title'] = 'NBDF Schlepp-App'
    context['weather'] = random.choice(possible_weather)
    return render_template('home.html',**context)

@app.route('/kontakt')
def about():
    context = global_context()
    return render_template('about.html',**context)

@app.route('/anmelden', methods=['POST', 'GET'])
def register():
    context = global_context()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        email = form.email.data
        token = serializer.dumps(email, salt='email-confirmation')
        confirmation_link = url_for('confirm_email', token=token, _external=True)
        user_data = {
            'firstname':form.firstname.data,
            'lastname':form.lastname.data,
            'email':form.email.data,
            'password':hashed_password,
            'confirmation_link':confirmation_link,
        }
        user = User(**user_data)
        msg = Message(
        'NBDF Anmeldung - Email bestätigen',
        sender=app.config['MAIL_USERNAME'],
        recipients=[email]
        )
        msg.body = f'Willkommen auf der NBDF Seite.\n\nBitte benutze diesen Link um deinen Account zu bestätigen: {confirmation_link.replace("localhost",server_IP)}\n\nBitte antworte nicht direkt auf diese Email.'
        mail.send(msg)
        db.session.add(user)
        db.session.commit()
        flash(f'Willkommen {form.firstname.data}, bitte bestätige die Email für deinen Account.','success')
        #context['user_email'] = form.email.data
        return redirect(url_for('login',**context))
    context['form'] = form
    context['title'] = 'Registrieren'
    return render_template('register.html',**context)

@app.route('/login', methods=['POST','GET'])
def login():
    context = global_context()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if request.method == 'POST':
        user = User.query.filter_by(email=form.email.data).first()
        if not user.is_validated:
            flash(Markup(f'Bitte bestätige erst deine Account, über den Link aus der Email. \n<a href="{url_for("resend_confirmation_link",email=user.email)}">Nochmal zusenden</a>'), 'danger')
            return redirect(url_for('home'))
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next','home')
            flash(f'Willkommen {current_user.firstname}.','success')
            return redirect(url_for(next_page.strip('/')))
        flash('Das hat nicht geklappt. Email oder Password sind nicht korrekt.', 'danger')
    context['form'] = form
    context['title'] = 'Einloggen'
    return render_template('login.html',**context)

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = serializer.loads(token, salt='email-confirmation', max_age=2*24*60*60)
        user = User.query.filter_by(email=email).first()
    except:
        flash('Der Bestätigungslink is abgelaufen','danger')
        return redirect(url_for('home'))
    user.is_validated = True
    db.session.commit()
    flash(f'Dein Account ist jetzt freigeschaltet {user.firstname}. Herzlich Willkommen.','success')
    return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    context = global_context()
    flash(f'Du bist ausgeloggt. Bis bald, {current_user.firstname}.','info')
    logout_user()
    return redirect(url_for('home'))

@app.route('/calendar')
def calendar():
    context = global_context()
    context['calendar_columwise'] = calendar_columwise
    return render_template('calendar.html',**context)

@app.route('/account')
@login_required
def account():
    context = global_context()
    # context['form'] = UpdateAccountForm()
    context['title'] = f'{current_user.firstname}\'s Account'
    context['image_file'] = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    return render_template('account.html',**context)

@app.route('/schleppinfo')
def schleppinfo():
    context = global_context()
    context['header_scripts'] += 'socket.io.min.js'.split(' ')
    context['body_scripts'] += 'socketio_infochat.js'.split(' ')
    context['weather'] = random.choice(possible_weather)
    return render_template('schleppinfo.html',**context)

@app.route('/resend_confirmation_link/<email>')
def resend_confirmation_link(email):
    user = User.query.filter_by(email=email).first()
    if user.is_validated:
        # Email-Spam verhindern
        return redirect(url_for('login'))
    email = user.email
    token = serializer.dumps(email, salt='email-confirmation')
    confirmation_link = url_for('confirm_email', token=token, _external=True)
    user.confirmation_link = confirmation_link
    db.session.commit()
    msg = Message(
    'NBDF Anmeldung - Email bestätigen',
    sender=app.config['MAIL_USERNAME'],
    recipients=[email]
    )
    msg.body = f'Willkommen auf der NBDF Seite.\n\nBitte benutze diesen Link um deinen Account zu bestätigen: {confirmation_link.replace("localhost",server_IP)}\n\nBitte antworte nicht direkt auf diese Email.'
    mail.send(msg)
    flash('Bestätigungs-Email erneut zugesandt','info')
    return redirect(url_for('login'))

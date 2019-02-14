from flask import Flask, request, flash, render_template, redirect, url_for
from flask_socketio import SocketIO, emit

from forms import RegistrationForm, LoginForm
from tools.calendar import make_example_set_of_assigned_fly_days

app = Flask(__name__)

app.config['SECRET_KEY'] = 'bfeedbcedf9edab2f6d29e657dd55f94ef2263a080732a0946'

socketio = SocketIO(app)

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
        flash(f'Account created for {form.firstname.data}!','success')
        return redirect(url_for('home')) # TODO: Better redirect
    context = {
        'form':form,
        'title':'Registrieren',
    }
    return render_template('register.html',**context)

@app.route('/login', methods=['POST','GET'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            #if <LOGIN-VALIDATOR>:
            flash(f'Wellcome {form.email.data}','success') # TODO: durch email durch fistname ersetzen
            return redirect(url_for('home')) # TODO: Better redirect
        else:
            flash('Das hat nicht geklappt.Email oder Password sind nicht korrekt.', 'danger')
    context = {
        'form':form,
        'title':'Einloggen',
    }
    return render_template('login.html',**context)

# if __name__ == '__main__':
#     socketio.run(app,debug=True)
#     app.run(debug=True) # TODO: Remove Debug!

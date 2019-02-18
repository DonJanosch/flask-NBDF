from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

from website import user

class RegistrationForm(FlaskForm):
    firstname = StringField('Vorname', validators= [
                                DataRequired(),
                                Length(min=2, max=20)])

    lastname = StringField('Nachname', validators= [
                                DataRequired(),
                                Length(min=2, max=20)])

    email = StringField('Email', validators= [
                            DataRequired(),
                            Email()])

    password = PasswordField('Password', validators=[
                                DataRequired()])

    confirm_password = PasswordField('Password bestätigen', validators=[
                                        DataRequired(),
                                        EqualTo('password')])

    submit = SubmitField('Registrieren')

    def validate_firstname(self,firstname):
        user_exists = user.find({
            'firstname':firstname.data,
            'lastname':self.lastname.data,
        })
        if len([u for u in user_exists])>0:
            raise ValidationError('Dieses Mitglied existiert bereits.')

    def validate_lastname(self,lastname):
        user_exists = user.find({
            'firstname':self.firstname.data,
            'lastname':lastname.data,
        })
        if len([u for u in user_exists])>0:
            raise ValidationError('Dieses Mitglied existiert bereits.')

    def validate_email(self,email):
        user_exists = user.find({
            'email':email.data,
        })
        if len([u for u in user_exists])>0:
            raise ValidationError('Diese Email-Addresse ist bereits vergeben.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators= [
                            DataRequired(),
                            Email()])

    password = PasswordField('Password', validators=[
                                DataRequired()])

    remember = BooleanField('Eingeloggt bleiben')

    submit = SubmitField('Einloggen')

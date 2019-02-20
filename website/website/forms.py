from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from website.models import User

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
        user = User.query.filter_by(firstname=firstname.data,lastname=self.lastname.data).first()
        if user:
            raise ValidationError('Dieses Mitglied existiert bereits.')

    def validate_lastname(self,lastname):
        user = User.query.filter_by(firstname=self.firstname.data,lastname=lastname.data).first()
        if user:
            raise ValidationError('Dieses Mitglied existiert bereits.')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Diese Emailaddresse ist bereits registriert.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators= [
                            DataRequired(),
                            Email()])

    password = PasswordField('Password', validators=[
                                DataRequired()])

    remember = BooleanField('Eingeloggt bleiben')

    submit = SubmitField('Einloggen')

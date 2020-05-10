from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    name = StringField('Your name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_again = PasswordField('Repeat password', validators=[DataRequired()])
    submit = SubmitField('To register')


class ChangePassForm(FlaskForm):
    name = StringField('Your login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_new = PasswordField('New password', validators=[DataRequired()])
    submit = SubmitField('change')


class AddDirsForm(FlaskForm):
    name = StringField('User name', validators=[DataRequired()])
    dir = StringField('Full folder name', validators=[DataRequired()])
    submit = SubmitField('Give access')

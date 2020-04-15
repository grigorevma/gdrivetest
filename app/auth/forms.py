from sanic_wtf import SanicForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import Required


class LoginForm(SanicForm):
    name = StringField('Name', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Sign In')


class RegisterForm(SanicForm):
    name = StringField('Name', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Submit')

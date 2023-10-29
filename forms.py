from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf.file import FileAllowed, FileField


class LoginForm(FlaskForm):
    username = StringField("Username", [DataRequired("Please enter your username.")])
    password = PasswordField("Password", [DataRequired()])
    remember = BooleanField("Remember Me", default=False)
    submit = SubmitField("Login")

class addProfileForm(FlaskForm):
    name = StringField('Display Name', [DataRequired()])
    description = StringField("Description", [DataRequired()])
    image = FileField('Add Display Image', [FileAllowed(['jpg', 'jpeg', 'png'], "Images Only!")])
    submit = SubmitField("Let's Dig IN!.")

class SignupForm(FlaskForm):
    name = StringField("Name", [DataRequired("Please enter your name."), Length(min=4, max=30)])
    email = EmailField("Email", [DataRequired()])
    username = StringField("Username", [DataRequired(), Length(min=4, max=30)])
    pword = PasswordField("Password", [DataRequired(), Length(min=8)])
    cnfword = PasswordField("Confirm Password", [DataRequired(), EqualTo('pword', message="Password should be same.")])
    submit = SubmitField("Signup")
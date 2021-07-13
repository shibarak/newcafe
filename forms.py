from wtforms import StringField, SubmitField, SelectField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import *
import email_validator

class CafeForm(FlaskForm):
    name = StringField('Cafe name', validators=[DataRequired()])
    image_url = StringField('Link to cafe image', validators=[DataRequired(), URL()])
    location = StringField('Neighborhood of cafe', validators=[DataRequired()])
    map_url = StringField('Cafe location on Google Maps (URL)', validators=[DataRequired(), URL()])
    coffee_price = StringField('Price for a small coffee', validators=[DataRequired()])
    seats = StringField('Number of seats', validators=[DataRequired()])
    has_wifi = SelectField('Has wifi', choices=[(1, 'True'), (0, "False")], validators=[DataRequired()])
    has_sockets = SelectField('Has power outlets', choices=[(1, 'True'), (0, "False")], validators=[DataRequired()])
    has_toilets = SelectField('Has toilets', choices=[(1, 'True'), (0, "False")], validators=[DataRequired()])
    can_take_calls = SelectField('Takes calls', choices=[(1, 'True'), (0, "False")], validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = StringField("User name (email)", validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class UserForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired()])
    email = StringField("Email address", validators=[DataRequired(), Email()])
    password = PasswordField("Choose a password",
                             validators=[DataRequired(), EqualTo('confirm', message="Passwords must match.")])
    confirm = PasswordField("Confirm password", validators=[DataRequired()])
    submit = SubmitField('Register')

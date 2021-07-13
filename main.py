from flask import Flask, render_template, redirect, url_for, flash, abort
from requests import request, post
from flask_bootstrap import Bootstrap
from forms import CafeForm, LoginForm, UserForm
from werkzeug.security import generate_password_hash, check_password_hash
import csv
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import email_validator
import config

CAFE_API = 'http://0.0.0.0:5001'
API_KEY = config.API_KEY
headers = {"Key": API_KEY}
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

##CONNECT TO DB
if os.environ.get("DATABASE_URL") == None:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)



class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)

    __hash__ = object.__hash__

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    def __eq__(self, other):
        '''
        Checks the equality of two `UserMixin` objects using `get_id`.
        '''
        if isinstance(other, UserMixin):
            return self.get_id() == other.get_id()
        return NotImplemented

    def __ne__(self, other):
        '''
        Checks the inequality of two `UserMixin` objects using `get_id`.
        '''
        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return not equal

# db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")



@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        if current_user.is_anonymous:
            flash(message="Oops! You must login or register to submit a new cafe.")
            return render_template("add.html", form=form)
        response = post(url=(CAFE_API + "/add"), data=form.data, headers=headers)
        response.raise_for_status()
        print(response.text)
        return render_template('add.html', form=CafeForm(), success=True)

    return render_template('add.html', form=form, success=False)


@app.route('/cafes')
def cafes():
    with request(method="GET", url=(CAFE_API + "/all"), headers=headers) as response:
        cafes = response.json()['cafes']
        print(cafes)
    return render_template('cafes.html', cafes=cafes)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash("Password incorrect. Please check password and try again")
                return render_template("login.html", form=form)
        else:
            flash("Email not found.")
            return render_template("login.html", form=form)
    return render_template('login.html', form=form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = UserForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        if User.query.filter_by(email=email).first():
            flash("An account is already registered with this email address.")
            return render_template("register.html", form=form)
        name = form.name.data.lower()
        password = generate_password_hash(password=form.password.data,
                                          method="pbkdf2:sha256",
                                          salt_length=8)
        user = User(name=name,
                    email=email,
                    password=password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('home'))

    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)

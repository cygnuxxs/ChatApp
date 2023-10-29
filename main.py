from flask import Flask, render_template, url_for, redirect, jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from PIL import Image
import io
import base64
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from forms import *

app = Flask(__name__)
app.config["SECRET_KEY"] = "Cygnuxxs"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

socketio = SocketIO(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)

class Friendship(db.Model):
    __tablename__ = 'friends'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    friend_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    status = db.Column(db.String(15), default = "pending")

class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), nullable=False, unique=True)
    description = db.Column(db.String(50))
    dp = db.Column(db.LargeBinary)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)

    friends = db.relationship('Friendship', backref = 'users', lazy = 'dynamic')

with app.app_context() as con:
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods = ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    err = None
    form = LoginForm()
    if form.validate_on_submit():
        user_by_name = User.query.filter_by(username = form.username.data).first()
        if user_by_name:
            if check_password_hash(user_by_name.password, form.password.data):
                login_user(user_by_name)
                return redirect(url_for('dashboard'))
            else:
                err = "Password is incorrect. Try Again."
        else:
            err = "Username is found in the database."
    return render_template('login.html', title = "Welcome Back", form = form, err = err)

@app.route('/signup', methods = ["GET", "POST"])
def signup():
    form = SignupForm()
    err = None
    if form.validate_on_submit():
        name = form.name.data
        username = form.username.data
        email = form.email.data
        password = form.cnfword.data
        user_email = User.query.filter_by(email = email).first()
        if user_email:
            err = "The entered email address is already in use."
        else:
            new_user = User(
                name = name,
                username = username,
                email = email,
                password = generate_password_hash(password, "pbkdf2:sha256")
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for('addProfile'))
    return render_template("signup.html", title = "Signup to Experience", form = form, err = err)

@app.route("/addProfile", methods = ['POST', "GET"])
@login_required
def addProfile():
    form = addProfileForm()
    user = User.query.get(current_user.get_id())
    if form.validate_on_submit():
        user.name = form.name.data
        user.description = form.description.data
        image_file = request.files['profile-photo']
        if image_file:
            image = Image.open(image_file)
            compressed_img = io.BytesIO()
            image.save(compressed_img, format="JPEG", optimize=True, quality = 40)
            image_data = compressed_img.getvalue()
            user.dp = image_data
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('profile.html', form = form, user = user)

@app.route("/checkUsername", methods = ["POST"])
def check():
    data = request.get_json()
    username = data.get("username")
    user = User.query.filter_by(username = username).first()
    if user:
        response = {"available" : False}
    else:
        response = {"available" : True}
    return jsonify(response)

@app.route('/userQuery', methods = ['POST'])
@login_required
def userQuery():
    username = request.form.get('username')
    user = User.query.filter(User.username.ilike(f"%{username}%")).first()
    if user:
        user_data = {
            'name' : user.name,
            'username' : user.username,
            'desc' : user.description
        }
        if user.dp:
            user_data["picture"] = base64.b64encode(user.dp).decode('utf-8')
        else:
            with app.open_resource('static/images/profil.png', 'rb') as photo:
                photo_data = photo.read()
            user_data['picture'] = base64.b64encode(photo_data).decode("utf-8")
        return jsonify(user = user_data)
    else:
        return jsonify(user = None)


@app.route("/", methods = ["GET", "POST"])
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('welcome.html', title = "Welcome to ChatApp")

@app.route("/dashboard", methods = ["GET", "POST"])
@login_required
def dashboard():
    return render_template('dashboard.html', title = "Dashboard")

@app.route('/logout', methods = ['GET', "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/rough', methods = ["GET", "POST"])
def rough():
    return render_template('rough.html')


if __name__ == "__main__":
    socketio.run(app, host="127.0.0.1", port=8000, debug=True)
import os, datetime, sys
from flask import Flask
from flask import render_template
from flask import request, session, redirect, flash, g
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from random import SystemRandom
from backports.pbkdf2 import pbkdf2_hmac, compare_digest
from flask.ext.login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property


app = Flask(__name__)

app.config.from_pyfile('fitgents.py')
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)

### Database table definitions ###

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column('user_id', db.Integer, primary_key=True)
	name = db.Column(db.String(50))
	email = db.Column(db.String(50))
	age = db.Column(db.Integer)
	food_history = db.relationship('FoodHistory', backref='user', lazy='dynamic')
	sleep_history = db.relationship('SleepHistory', backref='user', lazy='dynamic')
	excercise_history = db.relationship('ExcerciseHistory', backref='user', lazy='dynamic')
	_password = db.Column(db.LargeBinary(120))
	_salt = db.Column(db.String(120))

	@hybrid_property
	def password(self):
		return self._password

	# In order to ensure that passwords are always stored
	# hashed and salted in our database we use a descriptor
	# here which will automatically hash our password
	# when we provide it (i. e. user.password = "12345")
	@password.setter
	def set_password(self, value):
		# When a user is first created, give them a salt
		if self._salt is None:
			self._salt = bytes(SystemRandom().getrandbits(128))
		self._password = self._hash_password(value)

	def is_valid_password(self, password):
		"""Ensure that the provided password is valid.
		We are using this instead of a ``sqlalchemy.types.TypeDecorator``
		(which would let us write ``User.password == password`` and have the incoming
		``password`` be automatically hashed in a SQLAlchemy query)
		because ``compare_digest`` properly compares **all***
		the characters of the hash even when they do not match in order to
		avoid timing oracle side-channel attacks."""
		new_hash = self._hash_password(password)
		return compare_digest(new_hash, self._password)

	def _hash_password(self, password):
		pwd = password.encode("utf-8")
		salt = bytes(self._salt)
		buff = pbkdf2_hmac("sha512", pwd, salt, iterations=100000)
		return bytes(buff)

	def __repr__(self):
		return '<User %r>' % (self.name)
	
class FoodHistory(db.Model):
	__tablename__ = 'food_history'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	timestamp = db.Column(db.DateTime)
	
	
class SleepHistory(db.Model):
	__tablename__ = 'sleep_history'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	timestamp = db.Column(db.DateTime)
	
class ExcerciseHistory(db.Model):
	__tablename__ = 'excercise_history'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
	timestamp = db.Column(db.DateTime)

#############
# Application decorators

@app.before_request
def load_user():
	if "user_id" in session:
		user = User.query.filter_by(username=session["user_id"]).first()
		print "Found user in session: %s" % user.name
	else:
		user = {"name": "Guest"}
		print "Found no user in session, using Guest"
		
	g.user = user

@app.errorhandler(404)
def page_not_found(e):
	flash("Error 404 - Page Not Found", "danger")
	print str(e)
	return render_template('error.html')

@app.errorhandler(403)
def page_not_found(e):
	flash("Error 403 - Access Forbidden", "danger")
	print str(e)
	return render_template('error.html')

@app.errorhandler(410)
def page_not_found(e):
	flash("Error 410 - Page Gone", "danger")
	print str(e)
	return render_template('error.html')

@app.errorhandler(500)
def page_not_found(e):
	flash("Error 500 - Internal Server Error", "danger")
	print str(e)
	return render_template('error.html')

##############

@app.route("/")
@app.route("/index")
def index():
	return render_template("dashboard.html")

@app.route("/login")
def login():
	return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
	if request.method == "GET":
		if "user_id" in session:
			flash("We've detected that someone is already signed in, no need to register!", "info")
			return render_template("dashboard.html")
		else:
			return render_template("register.html")
	elif request.method == "POST":
		print "Detected POST request on registration page, processing new sign up."
		try:
			if request.form['inputName']:
				print "Attempting to create user " + request.form['inputName']
			new_user_name = request.form['inputName']
			new_user_email = request.form['inputEmail']
			new_user_age = request.form['inputAge']
			new_user_password = request.form['inputPassword']
			new_user_samepass = request.form['inputPassword']
			
			# verify passwords match
			if new_user_password == new_user_samepass:
				print "User is registering with matching passwords!"
				
				try:
					entry = User(name = new_user_name, email = new_user_email, age = new_user_age, password=new_user_password)
					
					db.session.add(entry)
					db.session.commit()
					
					flash("User registration for %s was successful!" % new_user_name, "success")
					return render_template("dashboard.html")
					
				except Exception as e:
					print str(e)
					flash("Error adding entry to the database, try again.", "warning")
					return render_template("register.html")
					
		except Exception as e:
			print str(e)
			flash("Error gathering data from the form in the POST request", "warning")
			return render_template("register.html")
			
	flash("Request made on registration that wasn't POST or GET, check the logs.", "warning")
	return render_template("register.html")

@app.route("/food")
@app.route("/<user>/food")
def food():
	return render_template("food.html")

@app.route("/excercise")
@app.route("/<user>/excercise")
def excercise():
	return render_template("excercise.html")

@app.route("/sleep")
@app.route("/<user>/sleep")
def sleep():
	return render_template("sleep.html")

@app.route("/statistics")
@app.route("/<user>/statistics")
def statistics():
	return render_template("statistics.html")

@app.route("/profile")
@app.route("/<user>/profile")
def profile():
	return render_template("profile.html")

if __name__ == "__main__":
	app.run(debug = "True", host="0.0.0.0")

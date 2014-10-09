import os, datetime, sys
from flask import Flask
from flask import render_template
from flask import request, session, redirect, flash, g, url_for
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from random import SystemRandom
from backports.pbkdf2 import pbkdf2_hmac, compare_digest
from flask.ext.login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property


app = Flask(__name__)

app.config.from_pyfile('fitgents.py')
db = SQLAlchemy(app)
#lm = LoginManager()
#lm.init_app(app)

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
	def password(self, value):
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
	calories = db.Column(db.Integer)
	protein = db.Column(db.Integer)
	fat = db.Column(db.Integer)
	notes = db.Column(db.String(300))
	
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
		user = User.query.filter_by(id=session["user_id"]).first()
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

@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "GET":
		if "user_id" in session:
			flash("Detected user %s already logged in!" % session["user_name"], "info")
			return render_template("login.html")
		else:
			return render_template("login.html")
	elif request.method == "POST":
		if request.form['inputEmail']:
			print "Attempting to log in user with email %s" % request.form['inputEmail']
			
			try:
				findUserResult = User.query.filter_by(email=request.form['inputEmail']).count()
				if findUserResult > 0:
					print "Found at least one user with email %s" % request.form['inputEmail']
					loginUser = User.query.filter_by(email=request.form['inputEmail']).first()
					
					print "Found a user to log in, checking entered password %s" % (request.form['inputPassword'])
					print loginUser.__dict__
					
					if loginUser.is_valid_password(request.form['inputPassword']):
						print "Passwork checks out! Logging in user"
						
						# set up session user
						session['user_id'] = loginUser.id
						session['user_name'] = loginUser.name
						session['user_email'] = loginUser.email
						
						# session user set up, redirect to dashboard, logged in
						return redirect(url_for("index"))
						
					else: # password check fails, redirect
						flash("Email or password was incorrect, try again", "warning")
						return redirect(url_for("login"))
						
				else:
					flash("No users with email %s found in the database" % request.form['inputEmail'], "warning")
					return render_template("login.html")
					
			except Exception as e:
				print str(e)
				flash("There was a problem logging in, check logs.", "warning")
				return redirect(url_for("login"))
		
		else:  # POST request with no data, or missing email address
			flash("No email address given in form, try again", "warning")
			return redirect(url_for("login"))
	
	else:  # HTTP request given, not a GET or POST though
		flash("HTTP request for login page detected, but method is not supported.", "warning")
		return redirect(url_for("index"))
		
@app.route("/logout")
def logout():
	session.clear()
	flash("Logged out successfully.", "success")
	return redirect(url_for("index"))

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
					findUsersQuery = User.query.all()
					for user in findUserQuery:
						if user.name == new_user_name:
							raise Exception
						if user.email == new_user_email:
							raise Exception
				except Exception as e:
					flash("User name or email has already been taken.", "info")
					return redirect(url_for("login"))
				
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
# TODO: Implement POST request for adding logs
def food():
	if "user_id" in session:
		try:
			#foodLogCount = FoodHistory.query.filter_by(id=session['user_id']).count()
			#if foodLogCount == 0:
			#	print "Did not find any food logs for user with user_id %d" % session['user_id']
			#	return render_template("food.html")
			#else:
			foodLogQuery = FoodHistory.query.filter_by(id=session['user_id'])
			print "Successfully queried the db for food history"
			g.user.foodlog = foodLogQuery
				
			return render_template("food.html")
		except Exception as e:
			print str(e)
			flash("There was a problem grabbing the food log from the database.", "warning")
			return redirect(url_for("food"))
			
	else:
		return render_template("food.html")

@app.route("/food/new", methods=["POST"])
def addfood():
	# start by attempting to fill all variables
	try:
		logDate = request.form['inputDate']
		logCalories = request.form['inputCalories']
		logProtein = request.form['inputProtein']
		logCarbohydrates = request.form['inputCarbohydrates']
		logFat = request.form['inputFat']
		logNotes = request.form['inputNotes']
	except Exception as e:
		print str(e)
		flash("There was an error pulling information from the form.", "warning")
		return redirect(url_for("food"))
		
	# set the timestamp if not already defined
	if not logDate:
		print "No date given in the form, adding manually"
		logDate = datetime.date.today()
		
	logEntry = FoodHistory(user_id = session['user_id'],
							calories = logCalories,
							protein = logProtein,
							fat = logFat,
							timestamp = logDate,
							notes = logNotes)
	try:
		db.session.add(logEntry)
		db.session.commit()
		
		flash("Food log submitted successfully!", "success")
		return redirect(url_for("food"))
	except Exception as e:
		print str(e)
		flash("There was an error submitting the food log.", "warning")
		return redirect(url_for("food"))

@app.route("/excercise")
# TODO: Implement POST request for adding logs
def excercise():
	return render_template("excercise.html")

@app.route("/sleep")
# TODO: Implement POST request for adding logs
def sleep():
	return render_template("sleep.html")

@app.route("/statistics")
def statistics():
	return render_template("statistics.html")

@app.route("/profile")
def profile():
	if "user_id" in session: # session token found
		return render_template("profile.html")
	else:
		flash("Must be logged in to view profiles.", "info")
		return redirect(url_for("index"))

if __name__ == "__main__":
	app.run(debug = "True", host="0.0.0.0")

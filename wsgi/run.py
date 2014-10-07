import os
from flask import Flask
from flask import render_template
from flask import request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

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
	start_weight = db.Column(db.Float)
	start_bf = db.Column(db.Float)
	age = db.Column(db.Integer)
	history = db.relationship('UserHistory', backref='user', lazy='dynamic')
	
	def __repr__(self):
		return '<User %r>' % (self.name)
	
class UserHistory(db.Model):
	__tablename__ = 'user_history'
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))

@app.route("/")
@app.route("/index")
def index():
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug = "True", host="0.0.0.0")

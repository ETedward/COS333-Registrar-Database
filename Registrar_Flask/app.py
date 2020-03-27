from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#from forms import RegistrationForm, LoginForm

app = Flask(__name__)
#
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
# db = SQLAlchemy(app)
#
#
# # create user model and add columns for the table
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key = True)
#
#     username = db.Column(db.String(20), unique = True, nullable = False)
#     email = db.Column(db.String(120), unique = True, nullable = False)
#     image_file = db.Column(db.String(20), nullable = False, default = 'default.jpg')
#     password = db.Column(db.String(60), nullable = False) # 60 char long hashed passwords
#     posts = db.relationship('Post', backref='author', lazy = True ) # relationship between Users and posts
#     # backref adds an author to the Post Model
#     # repr dunder / magic methods prints out our object
#     def __repr__(self):
#         return f"User('{self.username}','{self.email}','{self.image_file}')"
#
#
# class Post(db.Model): #another class inherited from db.Model
#     id = db.Column(db.Integerl, primary_keys = True)
#     title = db.Column(db.String(100), nullable = False)
#     date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
#     content = db.Column(db.Text, nullable = False)
#
#     def __repr__(self):
#         return f"Post('{self.title}','{self.date_posted}')"

@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/browse')
def browse():
    return render_template('browse.html')

@app.route('/analyze')
def analyze():
    return render_template('analyze.html')


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def serverproblem(e):
    return render_template('404.html'), 500


if __name__ == '__main__':
    app.run(debug=True)

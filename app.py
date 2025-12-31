from flask import Flask, render_template, redirect, url_for
from sqlmodel import SQLModel, Session, Field, create_engine
from flask_wtf import CSRFProtect
from email_validator import validate_email, EmailNotValidError
from dotenv import load_dotenv 
from datetime import datetime
from flask_mailman import EmailMultiAlternatives, Mail
from typing import List, Optional
import os

load_dotenv('.env')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = os.environ.get('MAIL_PORT')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER')
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS')
app.config['MAIL_RECIPIENT'] = os.environ.get('MAIL_RECIPIENT')
csrf = CSRFProtect(app)
mail = Mail(app)
db_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)



@app.route('/')
def home():
    return render_template('index.html', title='Portfolio of Soca Latchman')

@app.route('/about')
def about():
    pass

@app.route('/contact')
def contact():
    pass

@app.route('/resume')
def resume():
    pass

@app.route('/blog')
def blog():
    pass

@app.route('/blog/post/<post_id>')
def blog_post():
    pass

@app.route('/projects')
def projects():
    pass

@app.route('/dashboard/signin')
def signin():
    pass

@app.route('/dashboard')
def dashboard():
    pass


if __name__ == '__main__':
    app.run(debug=True)
from flask import Blueprint, app, render_template, request, flash, redirect, url_for , make_response
from flask_mail import Message
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from authlib.integrations.flask_client import OAuth
from . import oauth
import jsonify
import jwt
from functools import wraps
import datetime
import uuid
from . import create_app
import pyrebase
from .__init__ import DBNAME 
import logging
from . import mail
import random




 
#logging.basicConfig(filename = 'auth.log', level=logging.ERROR, format = '%(message)s%')








config = {
    "apiKey": "AIzaSyDh32Jqlnf_9iTFBpa7F_Qj-pYR2J8sR1A",
    "authDomain": "fireebasetest-1597a.firebaseapp.com",
    "databaseURL": f'sqlite:///{DBNAME}',
    "projectId": "fireebasetest-1597a",
    "storageBucket": "fireebasetest-1597a.appspot.com",
    "messagingSenderId": "865107738885",
    "appId": "1:865107738885:web:00350e25301a1e9377376c",
    "measurementId": "G-9KYNZDZDGP"
}

firebase = pyrebase.initialize_app(config)

a = firebase.auth()







auth = Blueprint('auth', __name__)



@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password , password):
                flash('Logged in successfully!', category='success')
                login_user(user)
                return redirect(url_for('main.profile'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    
    if request.method == 'POST':
        email = request.form.get('email')
        firstname = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(firstname) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            otp=random.randrange(100000,999999)
            print(otp)
            temp = str(otp)
            new_user = User(email=email, firstname=firstname, password=generate_password_hash(
            password1, method='sha256'),temp=generate_password_hash(temp,method='sha256'))
            
            

            db.session.add(new_user)
            
            db.session.commit()



        
            

            msg = Message('EMAIL_VERIFICATION', recipients=[new_user.email])
            print(new_user.email)
            temp = str(new_user.temp)
            msg.body = str(otp)

            mail.send(msg)
            
            return redirect(url_for('auth.verification'))
            

            
            
            
            

                      
            
            
            
            #login_user(new_user, remember=True)
            #flash('Account created!', category='success')
            #return redirect(url_for('auth.login'))

    return render_template("signup.html", user=current_user)


@auth.route('/login/google')
def google_login():
    google = oauth.create_client('google')
    redirect_uri = url_for('auth.google_authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@auth.route('/login/google/authorize')
def google_authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo').json()
    print(f"\n{resp}\n")
    return redirect(url_for('main.profile'))

@auth.route('/login/github')
def github_login():
    github = oauth.create_client('github')
    redirect_uri = url_for('auth.github_authorize', _external=True)
    return github.authorize_redirect(redirect_uri)

@auth.route('/login/github/authorize')
def github_authorize():
    github = oauth.create_client('github')
    token = github.authorize_access_token()
    resp = github.get('user').json()
    print(f"\n{resp}\n")
    return redirect(url_for('main.profile'))


@auth.route('/login/facebook')
def facebook_login():
    facebook = oauth.create_client('facebook')
    redirect_uri = url_for('auth.facebook_authorize', _external=True)
    return facebook.authorize_redirect(redirect_uri)

@auth.route('/login/facebook/authorize')
def facebook_authorize():
    facebook = oauth.create_client('facebook')
    token = facebook.authorize_access_token()
    resp = facebook.get('user').json()
    print(f"\n{resp}\n")
    return redirect(url_for('main.profile'))


@auth.route('/verify',methods=['GET','POST'])
def verification():
    if request.method == 'POST':
        email = request.form.get('email')
        OTP = request.form.get('OTP')
        

        user = User.query.filter_by(email=email).first()
        print(user.temp)
        if user:
            if check_password_hash(user.temp,OTP):
                flash('Account Verified!', category='success')
                user.verified = True
                login_user(user, remember=True)
                flash('Account created!', category='success')
                return redirect(url_for('auth.login'))
            else:
                flash('Incorrect OTP, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("verify.html")



     